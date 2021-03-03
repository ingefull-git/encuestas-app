from datetime import date

from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE
from django.utils.text import slugify
from django.utils.timezone import now



class Tag(models.Model):
    nombre = models.CharField(max_length=30, null=False, blank=False)
    creado = models.DateTimeField(default=date.today())
    modificado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre


class Encuesta(models.Model):
    pregunta = models.CharField(max_length=300, null=False, blank=False)
    creado = models.DateField(auto_now=True)
    vence = models.DateField(default=now().today())
    usuario = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, blank=True, null=True,
                            on_delete=models.SET_NULL)

    def __str__(self):
        return self.pregunta

    def total(self):
        return Respuesta.objects.filter(
            opcion__encuesta_id=self.id).count()

    def vencida(self):
        if self.vence < date.today():
            return True
        return False


class Opcion(models.Model):
    titulo = models.CharField(max_length=100, null=False, blank=False)
    creado = models.DateField(auto_now=True)
    encuesta = models.ForeignKey(Encuesta, on_delete=CASCADE)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = 'Opcion'
        verbose_name_plural = 'Opciones'


class Respuesta(models.Model):
    opcion = models.ForeignKey(Opcion, on_delete=CASCADE)
    creado = models.DateField(auto_now=True)
    slug = models.SlugField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        self.slug = slugify(self.opcion)
        super(Respuesta, self).save(*args, **kwargs)
