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

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'