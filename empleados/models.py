from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    ROL_CHOICES = (
        ('empleado', 'Empleado'),
        ('jefe', 'Jefe de departamento'),
    )
    rol = models.CharField(max_length=10, choices=ROL_CHOICES)
    departamento = models.CharField(max_length=50, blank=True, null=True)


class Mensaje(models.Model):
    remitente = models.ForeignKey(Usuario, related_name='enviados', on_delete=models.CASCADE)
    destinatario = models.ForeignKey(Usuario, related_name='recibidos', on_delete=models.CASCADE)
    asunto = models.CharField(max_length=100)
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)


class Horario(models.Model):
    empleado = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    dia = models.CharField(max_length=10)
    entrada = models.TimeField()
    salida = models.TimeField()
