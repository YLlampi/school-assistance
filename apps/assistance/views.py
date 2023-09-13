import json
from datetime import datetime, date, timedelta
from http import HTTPStatus

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from apps.assistance.models import Assistance, DetailAssistance
from apps.school.models import Course, Classroom
from apps.student.models import Student
from apps.teacher.models import Teacher

MONTHS = [
    "Enero",
    "Febrero",
    "Marzo",
    "Abril",
    "Mayo",
    "Junio",
    "Julio",
    "Agosto",
    "Septiembre",
    "Octubre",
    "Noviembre",
    "Diciembre"
]


# Create your views here.
class TakeAssistanceView(LoginRequiredMixin, TemplateView):
    template_name = 'assistance/assistance.html'
    login_url = reverse_lazy('users_app:user_login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher_obj = Teacher.objects.get(id=self.request.user.id)
        context['classrooms'] = teacher_obj.classrooms.all()
        return context


def register_assistance(request):
    if request.method == 'GET':
        data_request = request.GET.get('data')
        data = json.loads(data_request)

        dni = data['dni']
        first_name = str(data['first_name']).upper()
        last_name = str(data['last_name']).upper()
        grade = data['grade']
        section = str(data['section']).upper()
        code_generation = str(data['code_generation'])
        selected_classroom = int(data['selected_classroom'])
        classroom_obj = Classroom.objects.get(id=selected_classroom)
        teacher_obj = Teacher.objects.get(id=request.user.teacher.id)
        # level = str(data['level']).upper()

        if not dni or not first_name or not last_name or not grade or not section:
            return JsonResponse({
                'title': 'Error',
                'content': 'Datos incompletos'
            }, status=HTTPStatus.INTERNAL_SERVER_ERROR)

        try:
            student_obj = Student.objects.get(dni=dni)
            if student_obj.classroom.id != classroom_obj.id:
                return JsonResponse({
                    'title': 'Error de Aula',
                    'content': 'Alumno no Registrado en el aula',
                }, status=HTTPStatus.INTERNAL_SERVER_ERROR)
        except Exception as e:
            return JsonResponse({
                'title': 'Alumno no encontrado',
                'content': 'Registre en la base de datos',
                'error': str(e)
            }, status=HTTPStatus.INTERNAL_SERVER_ERROR)

        assistance_obj, is_created = Assistance.objects.get_or_create(
            code_generation=code_generation,
            defaults={
                'classroom': classroom_obj,
                'teacher': teacher_obj
            }
        )
        assistance_obj.save()

        detail_assistance_obj, is_created = DetailAssistance.objects.get_or_create(
            assistance=assistance_obj,
            student=student_obj
        )
        detail_assistance_obj.save()

        return JsonResponse({
            'dni': dni,
            'exito': 'Alumno Registrado Correctamente'
        }, status=HTTPStatus.OK)


class ReportAssistance(LoginRequiredMixin, TemplateView):
    template_name = 'assistance/report_assistance.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher_obj = Teacher.objects.get(id=self.request.user.teacher.id)
        classrooms = self.request.user.teacher.classrooms.all()
        context['classrooms'] = classrooms

        classroom_id = self.request.GET.get('classroom', '')
        date1 = self.request.GET.get('date1', '')
        date2 = self.request.GET.get('date2', '')

        assistances = Assistance.objects.filter(teacher=teacher_obj)
        students = Student.objects.all()
        attendance_data = []

        # Get the current date
        current_date = datetime.now().date()

        if classroom_id:
            classroom_obj = Classroom.objects.get(id=classroom_id)
            assistances = assistances.filter(
                classroom=classroom_obj,
            )
            students = students.filter(classroom=classroom_obj)

            for student in students:
                student_attendance = {
                    'student': student,
                    'attendance_dates': []
                }

                if date1 and date2:
                    assistances = assistances.filter(date__range=(date1, date2))
                else:
                    # Calculate the first day of the current month
                    first_day_of_current_month = date(current_date.year, current_date.month, 1)

                    # Calculate the last day of the current month
                    if current_date.month == 12:
                        last_day_of_current_month = date(current_date.year + 1, 1, 1) - timedelta(days=1)
                    else:
                        next_month = current_date.replace(month=current_date.month + 1, day=1)
                        last_day_of_current_month = next_month - timedelta(days=1)

                    assistances = assistances.filter(date__range=(first_day_of_current_month, last_day_of_current_month))

                for assistance in assistances:
                    # if DetailAssistance.objects.filter(student=student, assistance=assistance).exists():
                    #     student_attendance['attendance_dates'].append(True)
                    # else:
                    #     student_attendance['attendance_dates'].append(False)
                    is_present = DetailAssistance.objects.filter(
                        student=student,
                        assistance=assistance,
                    ).exists()
                    attendance_info = {
                        'is_present': is_present,
                        'css_class': 'success' if is_present else 'danger'
                    }
                    student_attendance['attendance_dates'].append(attendance_info)

                attendance_data.append(student_attendance)

        # if date1 and date2:
        #     assistances = assistances.filter(date__range=(date1, date2))

        context['current_month'] = MONTHS[current_date.month-1]
        context['current_year'] = current_date.year
        context['assistances'] = assistances
        context['students'] = students
        context['attendance_data'] = attendance_data

        return context
