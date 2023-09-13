import pandas as pd

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from apps.school.models import Classroom, Grade, Section
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


def import_xlsx(request):
    if request.method == 'POST':
        file = request.FILES['archivo_excel']
        if file.name.endswith('.xlsx'):
            df = pd.read_excel(file)
            for index, row in df.iterrows():
                dni = row['dni']
                first_name = row['first_name']
                last_name = row['last_name']
                grade = row['grade']
                section = row['section']

                grade_obj = Grade.objects.get(short_name=grade)
                section_obj = Section.objects.get(short_name=section)

                classroom_obj = Classroom.objects.get(grade=grade_obj, section=section_obj)
                student_obj = Student(
                    dni=dni,
                    first_name=first_name,
                    last_name=last_name,
                    classroom=classroom_obj
                )
                student_obj.save()
            return HttpResponse('Datos importados exitosamente.')
        else:
            return HttpResponse('El archivo debe estar en formato Excel (.xlsx).')
    return render(request, 'student/import_xlsx.html')