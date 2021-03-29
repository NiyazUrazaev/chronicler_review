from django.contrib import admin

# Register your models here.
from django.http import HttpResponseRedirect
from django.urls import path, reverse

from review_process.helpers import create_review
from review_process.models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    fields = (
        'name',
        'git_url',
        'description',
    )
    list_display = (
        'name',
        'git_url',
        'description',
    )
    list_filter = (
        'name',
        'git_url',
        'description',
    )

    change_form_template = 'admin_review_change.html'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('<project_id>/get_review/', self.admin_site.admin_view(self.get_review), name='get_review'),
        ]
        return my_urls + urls

    def get_review(self, request, project_id):

        project = Project.objects.get(id=project_id)
        result = create_review(project)

        return HttpResponseRedirect(
            reverse('admin:review_process_project_change',
                    kwargs={'object_id': project_id})
        )
