from django.db import models
from ..school.models import Classroom


# Create your models here.
class Student(models.Model):
    first_name = models.CharField('Nombre', max_length=50)
    last_name = models.CharField('Apellido', max_length=50)
    dni = models.CharField('DNI', max_length=8)

    classroom = models.ForeignKey(Classroom, verbose_name='Aula', on_delete=models.CASCADE)

    def get_fullname(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'
