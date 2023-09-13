from import_export.admin import ImportExportModelAdmin

from django.contrib import admin
from .models import Student


# Register your models here.


# class StudentAdmin(admin.ModelAdmin):
#     list_display = ('first_name', 'last_name', 'dni', 'classroom')
#
#
# admin.site.register(Student, StudentAdmin)

@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
    list_display = ('first_name', 'last_name', 'dni', 'classroom')
    search_fields = ('first_name', 'last_name', 'dni')
