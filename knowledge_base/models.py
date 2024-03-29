from django.db import models
from enum import Enum

# Create your models here.
from review_process.models import Project


class SetProjectMixin(models.Model):
    """Добавляем ссылку на проект"""

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        verbose_name='Проект, к которому относятся правила',
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True


class DjangoApps(models.Model):
    """
    Модель для перечисления модулей проекта
    """

    app_name_ru = models.CharField(
        max_length=128,
        verbose_name='Название модуля',
    )

    app_name_code = models.CharField(
        max_length=128,
        verbose_name='Название приложения в проекте',
    )

    description = models.TextField(
        verbose_name='Описание модуля',
        default='',
        blank=True,
    )

    def __str__(self):
        return f'{self.app_name_ru}'

    class Meta:
        verbose_name = 'Модуль проекта'
        verbose_name_plural = 'Модули проекта'


class DirectoryMixin(models.Model):
    """
    Миксин добавляющий отношение к какой директории относится правило
    """
    directory = models.ManyToManyField(
        DjangoApps,
        related_name='%(app_label)s_%(class)s_directories',
        verbose_name="Директории",
        blank=True,
    )

    class Meta:
        abstract = True


class AbbreviationRules(SetProjectMixin):
    """
    Модель для формирования базы знаний по соглашениям на аббревиатуры
    """

    MUST_BE = 1
    SHOULDNT_BE = 2

    ABBREVIATION_TYPES = (
        (MUST_BE, 'Присутсвует'),
        (SHOULDNT_BE, 'Не присутствует'),
    )

    tag_name_ru = models.CharField(
        max_length=128,
        verbose_name='Аббревиатура'
    )

    tag_name_code = models.CharField(
        max_length=128,
        verbose_name='Название аббревиатуры в коде',
    )

    abbreviation_type = models.IntegerField(
        choices=ABBREVIATION_TYPES,
        verbose_name='Тип аббревиатуры',
        null=True,
        blank=True,
    )

    description = models.TextField(
        verbose_name='Значение аббревиатуры',
        default='',
        blank=True,
    )

    directory = models.ManyToManyField(
        DjangoApps,
        related_name='%(app_label)s_%(class)s_directories',
        verbose_name="Директории",
        through='AbbreviationDirectories',
        blank=True,
    )

    class Meta:
        verbose_name = 'Аббревиатура'
        verbose_name_plural = 'Аббревиатуры'


class AbbreviationDirectories(models.Model):
    """
    Связующая аббревиатур и директорий
    """
    abbreviation = models.ForeignKey(
        AbbreviationRules,
        on_delete=models.CASCADE,
        verbose_name='Аббревиатура',

    )

    directory = models.ForeignKey(
        DjangoApps,
        on_delete=models.CASCADE,
        verbose_name='Директория',
    )

    class Meta:
        verbose_name = 'Дирекция, к которой относится аббревиатура'
        verbose_name_plural = 'Дирекции, к которым относится аббревиатура'


class ProjectFile(models.Model):
    """
    Файлы в проекте
    """
    file_name = models.CharField(
        max_length=128,
        verbose_name='Название файла',
    )

    description = models.TextField(
        verbose_name='Описание файла',
        default='',
        blank=True,
    )

    def __str__(self):
        return f'Id: {self.id}, {self.file_name}'

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'


class AppStructureRules(SetProjectMixin):
    """
    Модель для формирования базы знаний по соглашениям на структуру модуля
    """

    must_be_files = models.ManyToManyField(
        ProjectFile,
        verbose_name='Файлы, которые должны быть в модуле',
        through='AppStructureProjectFiles',
        blank=True,
    )

    directory = models.ManyToManyField(
        DjangoApps,
        related_name='%(app_label)s_%(class)s_directories',
        verbose_name="Директории",
        through='AppStructureDirectories',
        blank=True,
    )

    class Meta:
        verbose_name = 'Структура модуля'
        verbose_name_plural = 'Структуры модулей'


class AppStructureDirectories(models.Model):
    """
    Связующая структуры проекта и директорий
    """
    app_structure = models.ForeignKey(
        AppStructureRules,
        on_delete=models.CASCADE,
    )

    directory = models.ForeignKey(
        DjangoApps,
        on_delete=models.CASCADE,
        verbose_name='Директория',
    )

    class Meta:
        verbose_name = 'Директория, к которой относится правило'
        verbose_name_plural = 'Директории, к которым относятся правила'


class AppStructureProjectFiles(models.Model):
    """
    Связующая структуры проекта и директорий
    """
    app_structure = models.ForeignKey(
        AppStructureRules,
        on_delete=models.CASCADE,
    )

    project_file = models.ForeignKey(
        ProjectFile,
        on_delete=models.CASCADE,
        verbose_name='Файл в проекте',
    )

    class Meta:
        verbose_name = 'Файл, который должен быть в модуле'
        verbose_name_plural = 'Файлы, которые должны быть в модуле'


class ProjectStructureRules(SetProjectMixin):
    """
    Модель для формирования базы знаний по соглашениям на структуру проекта
    """
    root_directory = models.CharField(
        max_length=128,
        verbose_name='Корневая директория проекта',
    )

    apps_rules = models.ManyToManyField(
        AppStructureRules,
        related_name='%(app_label)s_%(class)s_related',
        verbose_name='Правила на модули',
    )

    class Meta:
        verbose_name = 'Структура проекта'
        verbose_name_plural = 'Структуры проектов'


class DocStringParams(models.Model):
    """
    Параметры для докстрингов
    """
    param_name = models.CharField(
        max_length=128,
        verbose_name='Название параметра',
    )

    description = models.TextField(
        verbose_name='Описание параметра',
        default='',
        blank=True,
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        verbose_name='Проект, к которому относятся правила',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Параметр для докстринга'
        verbose_name_plural = 'Параметры для докстрингов'


class DocStringMethodsRules(SetProjectMixin):
    """
    Модель для формирования базы знаний по соглашениям на структуру докстрингов у метода
    """
    must_be_params = models.ManyToManyField(
        DocStringParams,
        related_name='%(app_label)s_%(class)s_related',
        verbose_name='',
        blank=True,
    )

    class Meta:
        verbose_name = 'Комментарий у метода'
        verbose_name_plural = 'Комментарии у метода'


class APIRules(SetProjectMixin):
    """
    Модель для формирования базы знаний по правилам на структуру API
    """
    function_name = models.CharField(
        max_length=123,
        verbose_name='Название метода в API'
    )

    project_files = models.ManyToManyField(
        ProjectFile,
        verbose_name='Файлы, к которым относится правило',
        through='APIStructureProjectFiles',
        blank=True,
    )

    directory = models.ManyToManyField(
        DjangoApps,
        related_name='%(app_label)s_%(class)s_directories',
        verbose_name="Директории к которым относится правило",
        through='APIStructureDirectories',
        blank=True,
    )

    class Meta:
        verbose_name = 'Правило на структуру API'
        verbose_name_plural = 'Правила на структуру API'


class APIStructureProjectFiles(models.Model):
    """
    Связующая структуры API и директорий
    """
    api_rule = models.ForeignKey(
        APIRules,
        on_delete=models.CASCADE,
    )

    project_file = models.ForeignKey(
        ProjectFile,
        on_delete=models.CASCADE,
        verbose_name='Файл в проекте',
    )

    class Meta:
        verbose_name = 'Файл, к которому относится правило'
        verbose_name_plural = 'Файлы, к которым относится правило'


class APIStructureDirectories(models.Model):
    """
    Связующая структуры API и директорий
    """
    api_rule = models.ForeignKey(
        APIRules,
        on_delete=models.CASCADE,
    )

    directory = models.ForeignKey(
        DjangoApps,
        on_delete=models.CASCADE,
        verbose_name='Директория',
    )

    class Meta:
        verbose_name = 'Директория, к которой относится правило'
        verbose_name_plural = 'Директории, к которым относятся правила'


class Link(models.Model):

    link_name = models.CharField(
        max_length=123,
        verbose_name='Тип связи',
    )

    def __str__(self):
        return f'{self.link_name}'

    class Meta:
        verbose_name = 'Тип связи'
        verbose_name_plural = 'Типы связи'


class Notion(models.Model):

    notion_text = models.CharField(
        max_length=200,
        verbose_name='Понятие',
    )

    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание понятия'
    )

    next_notion = models.ManyToManyField(
        'Notion',
        verbose_name='Следующее понятие',
        through='NotionToNotion',
        related_name='%(app_label)s_%(class)s_notions',
    )

    def __str__(self):
        return self.notion_text

    class Meta:
        verbose_name = 'Понятие'
        verbose_name_plural = 'Понятия'


class NotionToNotion(models.Model):

    prev_notion = models.ForeignKey(
        Notion,
        on_delete=models.CASCADE,
        verbose_name='Предыдущее понятие',
        related_name='%(app_label)s_%(class)s_prev_notions',
    )

    next_notion = models.ForeignKey(
        Notion,
        on_delete=models.CASCADE,
        verbose_name='Следующее понятие',
        related_name='%(app_label)s_%(class)s_next_notions',
    )

    link_type = models.ForeignKey(
        Link,
        on_delete=models.CASCADE,
        verbose_name='Тип связи',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Следующее понятие'
        verbose_name_plural = 'Следующие понятия'