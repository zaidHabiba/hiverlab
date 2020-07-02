from django.contrib import admin
from app.models import *
from django.contrib.auth.models import Group

admin.site.unregister(Group)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'programs')
    list_filter = ('project_name', 'programs')

    def programs(self, obj):
        return ",".join([item.program_name for item in obj.programs_list])


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('program_name', 'project_name', 'password', 'always_running')
    list_filter = ('program_name', 'password', 'always_running')
