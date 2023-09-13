from django.db import models


# from ..teacher.models import Teacher


# Create your models here.
class Grade(models.Model):
    name = models.CharField('Nombre', max_length=20)
    short_name = models.CharField('Abreviatura', max_length=5)

    def __str__(self):
        return f'{self.name} ({self.short_name})'

    class Meta:
        verbose_name = 'Grado'
        verbose_name_plural = 'Grados'


class Section(models.Model):
    name = models.CharField('Nombre', max_length=20)
    short_name = models.CharField('Abreviatura', max_length=5)

    def __str__(self):
        return f'{self.name} ({self.short_name})'


    class Meta:
        verbose_name = 'Seccion'
        verbose_name_plural = 'Secciones'


class Classroom(models.Model):
    grade = models.ForeignKey(Grade, verbose_name='Grado', on_delete=models.CASCADE)
    section = models.ForeignKey(Section, verbose_name='Seccion', on_delete=models.CASCADE)

    # teachers = models.ManyToManyField(Teacher)

    def __str__(self):
        return f'{self.grade.short_name} - {self.section.short_name}'

    class Meta:
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'


class Course(models.Model):
    name = models.CharField('Nombre curso', max_length=50)
    short_name = models.CharField('Abreviatura', max_length=10)

    # teachers = models.ManyToManyField(Teacher)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
