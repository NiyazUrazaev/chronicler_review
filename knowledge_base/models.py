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
    tag_name_ru = models.CharField(
        max_length=128,
        verbose_name='Аббревиатура'
    )

    tag_name_code = models.CharField(
        max_length=128,
        verbose_name='Название аббревиатуры в коде',
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
        verbose_name = 'Отношение аббревиатуры и дирекции'
        verbose_name_plural = 'Отношения аббревиатур и дирекций'


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
