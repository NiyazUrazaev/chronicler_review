import git
import os
import re

from django.conf import settings
from git import Repo

from knowledge_base.models import ProjectStructureRules, DocStringParams, AbbreviationRules
from review_process.models import ExceptionTypes


def get_all_commits(repo):
    commits = list(repo.iter_commits())
    commit_diffs = {}
    for index, commit in enumerate(commits[:10]):
        next_index = index + 1
        if next_index < len(commits):
            commit_diffs[commit.hexsha] = {
                'author': commit.author.name,
                'message': commit.message.strip(),
                'diff': repo.git.diff(commits[next_index], commit)
            }
    return commit_diffs


# commit_diffs = get_all_commits(repo)
# print(repo.untracked_files)


def check_for_structure_rules(project_structure_rules, repo_dir):
    """Проверка на наличие файлов в модуле"""
    exceptions = {}
    for rule in project_structure_rules:
        exceptions[rule.project.name] = []
        for app_rule in rule.apps_rules.all():
            for directory in app_rule.directory.all():
                if rule.root_directory and rule.root_directory != '.':
                    repo_dir = os.path.join(repo_dir, rule.root_directory)
                checked_dir = os.path.join(repo_dir, directory.app_name_code)
                try:
                    files_in_dir = os.listdir(checked_dir)
                except FileNotFoundError:
                    print(f'WARNING: Not existing directory: {checked_dir}')
                    continue
                for file in app_rule.must_be_files.all():
                    if file.file_name not in files_in_dir:
                        exception_message = f'В директории {directory} нет файла {file.file_name}'
                        exceptions[rule.project.name].append({
                            'exception_message': exception_message,
                            'exception_type': ExceptionTypes.PROJECT_STRUCTURE
                        })

    return exceptions


def check_for_docstring_rules(docstring_rules, repo_dir):
    """Проверка на docstring"""

    exceptions = {}
    excluded_files = [
        'manage.py',
        # Only for testing
        'views.py',
        'models.py',
    ]
    for rule in docstring_rules:
        exceptions[rule.project.name] = []

        for root, subdirs, files in os.walk(repo_dir):
            for filename in files:
                if filename in excluded_files:
                    continue
                file_path = os.path.join(root, filename)
                with open(file_path, 'r') as f:
                    try:
                        f_content = f.read()
                    except UnicodeDecodeError:
                        print(f'WARNING: Unicode decode at {file_path}')
                        continue
                    docstrings = re.findall(r'\"\"\".+\"\"\"', f_content)
                    for string in docstrings:
                        if rule.param_name not in string:
                            exception_path = file_path.split('clonned_repos')[-1]
                            exception_message = f'В файле {exception_path}, строковой документации {string}, нет параметра {rule.param_name}'
                            exceptions[rule.project.name].append({
                                'exception_message': exception_message,
                                'exception_type': ExceptionTypes.DOC_STRING_PARAMS
                            })

    return exceptions


def check_for_abbreviation_rules(abbreviation_rules, repo_dir):
    """Проверка на аббревиатуры"""

    exceptions = {}
    # Only for testing
    excluded_files = [
        'manage.py',
        'views.py',
        'models.py',
        '__init__.py',
    ]
    for rule in abbreviation_rules:
        exceptions[rule.project.name] = []
        for rule_directory in rule.abbreviationdirectories_set.all():
            repo_dir = os.path.join(repo_dir, rule_directory.directory.app_name_code)
            for root, subdirs, files in os.walk(repo_dir):
                exception_message = ''
                for filename in files:
                    if filename in excluded_files:
                        continue
                    file_path = os.path.join(root, filename)
                    with open(file_path, 'r') as f:
                        try:
                            f_content = f.read()
                        except UnicodeDecodeError:
                            print(f'WARNING: Unicode decode at {file_path}')
                            continue

                        exception_path = file_path.split('clonned_repos')[-1]
                        if rule.abbreviation_type == AbbreviationRules.MUST_BE and rule.tag_name_code not in f_content:
                            exception_message = f'В файле {exception_path}, не содержится аббревиатура {rule.tag_name_code}'
                        elif rule.abbreviation_type == AbbreviationRules.SHOULDNT_BE and rule.tag_name_code in f_content:
                            exception_message = f'В файле {exception_path}, присутсвует аббревиатура {rule.tag_name_code}'

                        if exception_message:
                            exceptions[rule.project.name].append({
                                'exception_message': exception_message,
                                'exception_type': ExceptionTypes.ABBREVIATION_RULE
                            })

    return exceptions


def create_review(projects_qs):
    """Проведение анализа проекта"""

    def _merge_two_dicts(x, y):
        z = x.copy()
        for key, value in y.items():
            if key not in z:
                z[key] = value
            else:
                z[key].extend(value)
        return z

    review_result = {}
    repo_dir = os.path.join(settings.BASE_DIR, 'clonned_repos')

    for project in projects_qs:
        # В зависимости от того есть у нас репа или нет
        # выполняем команды git clone или git pull
        if project.name not in os.listdir(repo_dir):
            repo_dir = os.path.join(repo_dir, project.name)
            os.mkdir(repo_dir)
            Repo.clone_from(project.git_url, repo_dir)
        else:
            repo_dir = os.path.join(repo_dir, project.name)
            git.cmd.Git(repo_dir).pull()

        # Проверка на структуру проекта
        project_structure_rules = ProjectStructureRules.objects.filter(project=project)
        review_result.update(_merge_two_dicts(review_result, check_for_structure_rules(project_structure_rules, repo_dir)))

        # Проверка на докстринги
        docstring_rules = DocStringParams.objects.filter(project=project)
        review_result.update(_merge_two_dicts(review_result, check_for_docstring_rules(docstring_rules, repo_dir)))

        # Проверка на аббревиатуры
        abbreviation_rules = AbbreviationRules.objects.filter(project=project)
        review_result.update(_merge_two_dicts(review_result, check_for_abbreviation_rules(abbreviation_rules, repo_dir)))

        repo = Repo(repo_dir)

    return review_result


