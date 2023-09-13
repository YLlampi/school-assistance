from django.contrib import admin
from .models import Grade, Section, Classroom, Course

# Register your models here.


admin.site.register(Grade)
admin.site.register(Section)


class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('id', 'grade', 'section')


admin.site.register(Classroom, ClassroomAdmin)
admin.site.register(Course)
