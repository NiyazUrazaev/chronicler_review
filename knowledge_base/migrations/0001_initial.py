# Generated by Django 3.1.7 on 2021-03-22 14:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AbbreviationDirectories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Отношение аабревиатуры и дирекции',
                'verbose_name_plural': 'Отношения аабревиатур и дирекций',
            },
        ),
        migrations.CreateModel(
            name='AppStructureDirectories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Отношение абревиатуры и дирекции',
                'verbose_name_plural': 'Отношения абревиатур и дирекций',
            },
        ),
        migrations.CreateModel(
            name='AppStructureProjectFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Отношение абревиатуры и дирекции',
                'verbose_name_plural': 'Отношения абревиатур и дирекций',
            },
        ),
        migrations.CreateModel(
            name='AppStructureRules',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Структура модуля',
                'verbose_name_plural': 'Структуры модулей',
            },
        ),
        migrations.CreateModel(
            name='DjangoApps',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_name_ru', models.CharField(max_length=128, verbose_name='Название раздела')),
                ('app_name_code', models.CharField(max_length=128, verbose_name='Название приложения в проекте')),
                ('description', models.TextField(blank=True, default='', verbose_name='Описание раздела')),
            ],
            options={
                'verbose_name': 'Модуль проекта',
                'verbose_name_plural': 'Модули проекта',
            },
        ),
        migrations.CreateModel(
            name='DocStringParams',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('param_name', models.CharField(max_length=128, verbose_name='Название параметра')),
                ('description', models.TextField(blank=True, default='', verbose_name='Описание параметра')),
            ],
            options={
                'verbose_name': 'Параметр для докстринга',
                'verbose_name_plural': 'Параметры для докстрингов',
            },
        ),
        migrations.CreateModel(
            name='ProjectFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=128, verbose_name='Название файла')),
                ('description', models.TextField(blank=True, default='', verbose_name='Описание файла')),
            ],
            options={
                'verbose_name': 'Файл',
                'verbose_name_plural': 'Файлы',
            },
        ),
        migrations.CreateModel(
            name='ProjectStructureRules',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('root_directory', models.CharField(max_length=128, verbose_name='Корневая директория проекта')),
                ('apps_rules', models.ManyToManyField(related_name='knowledge_base_projectstructurerules_related', to='knowledge_base.AppStructureRules', verbose_name='Правила на модули')),
            ],
            options={
                'verbose_name': 'Структура проекта',
                'verbose_name_plural': 'Структуры проектов',
            },
        ),
        migrations.CreateModel(
            name='DocStringMethodsRules',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('must_be_params', models.ManyToManyField(blank=True, related_name='knowledge_base_docstringmethodsrules_related', to='knowledge_base.DocStringParams', verbose_name='')),
            ],
            options={
                'verbose_name': 'Комментарий у метода',
                'verbose_name_plural': 'Комментарии у метода',
            },
        ),
        migrations.AddField(
            model_name='appstructurerules',
            name='directory',
            field=models.ManyToManyField(blank=True, related_name='knowledge_base_appstructurerules_directories', through='knowledge_base.AppStructureDirectories', to='knowledge_base.DjangoApps', verbose_name='Директории'),
        ),
        migrations.AddField(
            model_name='appstructurerules',
            name='must_be_files',
            field=models.ManyToManyField(blank=True, through='knowledge_base.AppStructureProjectFiles', to='knowledge_base.ProjectFile', verbose_name='Файлы, которые должны быть в модуле'),
        ),
        migrations.AddField(
            model_name='appstructureprojectfiles',
            name='app_structure',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='knowledge_base.appstructurerules'),
        ),
        migrations.AddField(
            model_name='appstructureprojectfiles',
            name='project_file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='knowledge_base.projectfile', verbose_name='Файл в проекте'),
        ),
        migrations.AddField(
            model_name='appstructuredirectories',
            name='app_structure',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='knowledge_base.appstructurerules'),
        ),
        migrations.AddField(
            model_name='appstructuredirectories',
            name='directory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='knowledge_base.djangoapps', verbose_name='Директория'),
        ),
        migrations.CreateModel(
            name='AbbreviationRules',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name_ru', models.CharField(max_length=128, verbose_name='Аббревиатура')),
                ('tag_name_code', models.CharField(max_length=128, verbose_name='Название аббревиатуры в коде')),
                ('description', models.TextField(blank=True, default='', verbose_name='Значение аббревиатуры')),
                ('directory', models.ManyToManyField(blank=True, related_name='knowledge_base_abbreviationrules_directories', through='knowledge_base.AbbreviationDirectories', to='knowledge_base.DjangoApps', verbose_name='Директории')),
            ],
            options={
                'verbose_name': 'Аббревиатура',
                'verbose_name_plural': 'Аббревиатуры',
            },
        ),
        migrations.AddField(
            model_name='abbreviationdirectories',
            name='abbreviation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='knowledge_base.abbreviationrules', verbose_name='Аббревиатура'),
        ),
        migrations.AddField(
            model_name='abbreviationdirectories',
            name='directory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='knowledge_base.djangoapps', verbose_name='Директория'),
        ),
    ]