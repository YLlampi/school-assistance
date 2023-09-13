from django.db import models
from ..school.models import Classroom
from ..teacher.models import Teacher
from ..student.models import Student


# Create your models here.
class Assistance(models.Model):
    date = models.DateField(auto_now_add=True)
    classroom = models.ForeignKey(Classroom, verbose_name='Aula', on_delete=models.SET_NULL, null=True)
    teacher = models.ForeignKey(Teacher, verbose_name='Profesor', on_delete=models.SET_NULL, null=True)
    code_generation = models.CharField('Codigo unico', max_length=50, unique=True)

    def get_day(self):
        return self.date.strftime('%d')

    def __str__(self):
        return f'{self.date}/{self.classroom}/{self.teacher.user.first_name}'

    class Meta:
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'


class DetailAssistance(models.Model):
    assistance = models.ForeignKey(Assistance, verbose_name='Asistencia', related_name='detailAssistance',
                                   on_delete=models.CASCADE, null=True, blank=True)
    time = models.TimeField(auto_now_add=True, verbose_name='Hora')
    student = models.ForeignKey(Student, verbose_name='Estudiante', related_name='detailAssistance',
                                on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.assistance.date}/{self.time}/{self.student.first_name}'

    class Meta:
        verbose_name = 'Detalle de Asistencia'
        verbose_name_plural = 'Detalle de Asistencias'
