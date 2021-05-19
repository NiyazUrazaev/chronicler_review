from django.contrib import admin

from django.template.response import TemplateResponse
from django.urls import path

from review_process.helpers import create_review
from review_process.models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    fields = (
        'name',
        'git_url',
        'root_directory',
        'description',
    )
    list_display = (
        'name',
        'git_url',
        'root_directory',
        'description',
    )
    list_filter = (
        'name',
        'git_url',
        'description',
    )

    change_form_template = 'admin_review_change.html'
    change_list_template = 'admin_review_list.html'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('get_all_review/', self.admin_site.admin_view(self.get_all_review), name='get_all_review'),
            path('<project_id>/get_review/', self.admin_site.admin_view(self.get_review), name='get_review'),
        ]
        return my_urls + urls

    def get_review(self, request, project_id):
        """Провести анализ одного проекта"""
        project = Project.objects.get(id=project_id)
        result = create_review([project])

        return TemplateResponse(request, 'analyse_result.html', {'data': result.items()})

    def get_all_review(self, request):
        """Провести анализ всех проектов"""
        projects_qs = Project.objects.all()
        result = create_review(projects_qs)

        return TemplateResponse(request, 'analyse_result.html', {'data': result.items()})
