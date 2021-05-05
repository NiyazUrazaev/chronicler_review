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

    def __str__(self):
        return f'Id: {self.id}, {self.name}'

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'


class ExceptionTypes(Enum):

    PROJECT_STRUCTURE = 'Структура проекта'
    DOC_STRING_PARAMS = 'Параметр в строковой документации'
    ABBREVIATION_RULE = 'Правило на аббревиатуру'