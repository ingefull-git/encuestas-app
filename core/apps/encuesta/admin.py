from django.contrib import admin

from .models import Encuesta, Opcion, Tag, Respuesta

# Register your models here.
admin.site.register(Encuesta)
admin.site.register(Tag)
admin.site.register(Opcion)
admin.site.register(Respuesta)
