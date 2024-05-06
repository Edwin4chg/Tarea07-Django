from django.db import models

# Create your models here.
class Evento(models.Model):
    nombre = models.CharField(max_length=400)
    descripcion = models.TextField()
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    ubicacion = models.CharField(max_length=300)
    capacidad_maxima = models.PositiveIntegerField()

    def __str__(self):
        return f"Nombre: {self.nombre}, Descripción: {self.descripcion}, Fecha de inicio: {self.fecha_inicio}, Fecha de fin: {self.fecha_fin}, Ubicación: {self.ubicacion}, Capacidad máxima: {self.capacidad_maxima}"


class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    correo_electronico = models.EmailField()
    contraseña = models.CharField(max_length=130)
    eventos = models.ManyToManyField(Evento, through='RegistroEvento')

    def __str__(self):
        return f"Nombre: {self.nombre}, Correo electrónico: {self.correo_electronico}, Contraseña: {self.contraseña}"


class RegistroEvento(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Usuario: {self.usuario.nombre}, Evento: {self.evento.nombre}, Fecha de registro: {self.fecha_registro}"
