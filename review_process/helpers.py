import git
import os

from django.conf import settings
from git import Repo

from knowledge_base.models import ProjectStructureRules


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
    exceptions = ''
    for rule in project_structure_rules:
        for app_rule in rule.apps_rules.all():
            for directory in app_rule.directory.all():
                checked_dir = os.path.join(repo_dir, directory.app_name_code)
                try:
                    files_in_dir = os.listdir(checked_dir)
                except FileNotFoundError:
                    print('Not existing directory')
                    continue
                for file in app_rule.must_be_files.all():
                    if file.file_name not in files_in_dir:
                        # exceptions
                        print(f'Warning: module has not file {file.file_name}')

    return exceptions


def create_review(project):
    """Проведение анализа проекта"""

    # В зависимости от того есть у нас репа или нет
    # выполняем команды git clone или git pull
    repo_dir = os.path.join(settings.BASE_DIR, 'clonned_repos')
    if project.name not in os.listdir(repo_dir):
        repo_dir = os.path.join(repo_dir, project.name)
        os.mkdir(repo_dir)
        Repo.clone_from(project.git_url, repo_dir)
    else:
        repo_dir = os.path.join(repo_dir, project.name)
        git.cmd.Git(repo_dir).pull()

    project_structure_rules = ProjectStructureRules.objects.filter(project=project)
    exceptions = check_for_structure_rules(project_structure_rules, repo_dir)


    repo = Repo(repo_dir)

    return repo


