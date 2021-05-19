from enum import Enum

from django.db import models

# Create your models here.


class Project(models.Model):
    """Модель для добавления проектов к анализу"""

    name = models.CharField(
        max_length=128,
        verbose_name='Название проекта',
    )

    description = models.TextField(
        verbose_name='Описание проекта',
        default='',
        blank=True,
    )

    git_url = models.URLField(
        verbose_name='Ссылка на репозиторий',
    )

    root_directory = models.CharField(
        max_length=123,
        verbose_name='Корневая директория',
        null=True,
        blank=True,
    )

    notions = models.ManyToManyField(
        'knowledge_base.Notion',
        verbose_name='Понятия',
        through='ProjectToNotion',
        related_name='%(app_label)s_%(class)s_notions',
    )

    def __str__(self):
        return f'Id: {self.id}, {self.name}'

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'


class ProjectToNotion(models.Model):

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        verbose_name='Предыдущее понятие',
    )

    notion = models.ForeignKey(
        'knowledge_base.Notion',
        on_delete=models.CASCADE,
        verbose_name='Понятие',
    )

    link_type = models.ForeignKey(
        'knowledge_base.Link',
        on_delete=models.CASCADE,
        verbose_name='Тип связи',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Понятия'
        verbose_name_plural = 'Понятия'


class ExceptionTypes(Enum):

    PROJECT_STRUCTURE = 'Структура проекта'
    DOC_STRING_PARAMS = 'Параметр в строковой документации'
    ABBREVIATION_RULE = 'Правило на аббревиатуру'
    API_RULE = 'Правило на структуру API'
