from django.contrib import admin
from .models import Assistance, DetailAssistance


# Register your models here.


class AssistanceAdmin(admin.ModelAdmin):
    list_display = ('date', 'classroom', 'teacher', 'code_generation')


admin.site.register(Assistance, AssistanceAdmin)


class DetailAssistanceAdmin(admin.ModelAdmin):
    list_display = ('assistance', 'time', 'student')


admin.site.register(DetailAssistance, DetailAssistanceAdmin)
