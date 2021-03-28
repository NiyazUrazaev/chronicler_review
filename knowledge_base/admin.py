from django import forms
from django.contrib import admin

# Register your models here.
from knowledge_base.models import (
    DjangoApps, AbbreviationRules,
    ProjectFile, AppStructureRules,
    ProjectStructureRules, DocStringParams,
    DocStringMethodsRules, AbbreviationDirectories, AppStructureDirectories, AppStructureProjectFiles,
)

admin.site.register(AbbreviationDirectories)
admin.site.register(DjangoApps)
admin.site.register(ProjectFile)
admin.site.register(ProjectStructureRules)
admin.site.register(DocStringParams)
admin.site.register(DocStringMethodsRules)


class AbbreviationDirectoriesInline(admin.TabularInline):
    fields = (
        'directory',
        'directory_app_name_ru',
        'directory_app_name_code',
        'directory_description',
    )
    readonly_fields = (
        'abbreviation',
        'directory_app_name_ru',
        'directory_app_name_code',
        'directory_description',
    )
    extra = 0

    model = AbbreviationDirectories

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('directory')

    def directory_app_name_ru(self, obj):
        if obj and obj.directory:
            return obj.directory.app_name_ru
        return self.get_empty_value_display()

    directory_app_name_ru.short_description = 'Название раздела'

    def directory_app_name_code(self, obj):
        if obj and obj.directory:
            return obj.directory.app_name_code
        return self.get_empty_value_display()

    directory_app_name_code.short_description = 'Название приложения в проекте'

    def directory_description(self, obj):
        if obj and obj.directory:
            return obj.directory.description
        return self.get_empty_value_display()

    directory_description.short_description = 'Описание раздела'

    def has_add_permission(self, request, obj=None):
        return True


@admin.register(AbbreviationRules)
class AbbreviationRulesAdmin(admin.ModelAdmin):
    fields = (
        'tag_name_ru',
        'tag_name_code',
        'description',
    )
    list_display = (
        'tag_name_ru',
        'tag_name_code',
        'description',
    )
    list_filter = (
        'directory',
    )
    inlines = (
        AbbreviationDirectoriesInline,
    )


class AppStructureInline(admin.TabularInline):
    fields = (
        'directory',
        'directory_app_name_ru',
        'directory_app_name_code',
        'directory_description',
    )
    readonly_fields = (
        'app_structure',
        'directory_app_name_ru',
        'directory_app_name_code',
        'directory_description',
    )
    extra = 0

    model = AppStructureDirectories

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('directory')

    def directory_app_name_ru(self, obj):
        if obj and obj.directory:
            return obj.directory.app_name_ru
        return self.get_empty_value_display()

    directory_app_name_ru.short_description = 'Название раздела'

    def directory_app_name_code(self, obj):
        if obj and obj.directory:
            return obj.directory.app_name_code
        return self.get_empty_value_display()

    directory_app_name_code.short_description = 'Название приложения в проекте'

    def directory_description(self, obj):
        if obj and obj.directory:
            return obj.directory.description
        return self.get_empty_value_display()

    directory_description.short_description = 'Описание раздела'

    def has_add_permission(self, request, obj=None):
        return True


class AppStructureFilesInline(admin.TabularInline):
    fields = (
        'project_file',
        'project_file_file_name',
        'project_file_description',
    )
    readonly_fields = (
        'app_structure',
        'project_file_file_name',
        'project_file_description',
    )
    extra = 0

    model = AppStructureProjectFiles

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('project_file')

    def project_file_file_name(self, obj):
        if obj and obj.project_file:
            return obj.project_file.file_name
        return self.get_empty_value_display()

    project_file_file_name.short_description = 'Название файла'

    def project_file_description(self, obj):
        if obj and obj.project_file:
            return obj.project_file.description
        return self.get_empty_value_display()

    project_file_description.short_description = 'Назначение файла'

    def has_add_permission(self, request, obj=None):
        return True


@admin.register(AppStructureRules)
class AppStructureRulesAdmin(admin.ModelAdmin):
    fields = (
        'app_names',
    )
    list_display = (
        'app_names',
    )
    list_filter = (
        'directory',
        'must_be_files'
    )
    readonly_fields = (
        'app_names',
    )
    inlines = (
        AppStructureFilesInline,
        AppStructureInline,
    )

    def app_names(self, obj):
        if obj and obj.directory.all().exists():
            return ', '.join(obj.directory.values_list('app_name_ru', flat=True))
        return self.get_empty_value_display()

    app_names.short_description = 'Названиея модулей'

