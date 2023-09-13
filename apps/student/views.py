from django.shortcuts import render
from django.views.generic import TemplateView

from apps.school.models import Classroom
from apps.student.models import Student


# Create your views here.
class GenerateQrView(TemplateView):
    template_name = 'student/generate_qr.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        students = Student.objects.all()
        classrooms = Classroom.objects.all()

        context['students'] = students
        context['classrooms'] = classrooms

        return context