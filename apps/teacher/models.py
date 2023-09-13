from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.school.models import Classroom, Course


# Create your models here.

class Teacher(models.Model):
    user = models.OneToOneField(User, verbose_name='Usuario', related_name='teacher', on_delete=models.CASCADE)
    dni = models.CharField('DNI', max_length=8, blank=True, null=True)

    classrooms = models.ManyToManyField(Classroom, verbose_name='Aulas')
    courses = models.ManyToManyField(Course, verbose_name='Cursos')

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    class Meta:
        verbose_name = 'Profesor'
        verbose_name_plural = 'Profesores'


@receiver(post_save, sender=User)
def create_user_teacher(sender, instance, created, **kwargs):
    if created:
        Teacher.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_teacher(sender, instance, **kwargs):
    instance.teacher.save()
