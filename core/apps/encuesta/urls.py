from django.contrib.auth.decorators import login_required
from django.urls import path

from core.apps.encuesta.views import (
    ListaEncuesta,
    nuevaEncuesta,
    modificaEncuesta,
    ResuladoEncuesta,
    BorraEncuesta,
    ListaTag,
    NuevoTag,
    BorraTag,
    ListaReporte,
    nuevaRespuesta,
)

app_name = 'encuesta'

urlpatterns = [

    path('nueva/', login_required(nuevaEncuesta), name='nueva-pregunta'),
    path('editar/<int:pk>/',
         login_required(modificaEncuesta), name='modifica-pregunta'),
    path('respuesta/<int:pk>/',
         nuevaRespuesta, name='responde-pregunta'),
    path('resultado/<int:pk>/',
         login_required(ResuladoEncuesta.as_view()), name='resultado-pregunta'),
    path('borrar/<int:pk>/',
         login_required(BorraEncuesta.as_view()), name='borra-pregunta'),

    path('tag/listado/', login_required(ListaTag.as_view()), name='lista-tag'),
    path('tag/nuevo/', login_required(NuevoTag.as_view()), name='nuevo-tag'),
    path('tag/borrar/<int:pk>/',
         login_required(BorraTag.as_view()), name='borra-tag'),

    path('reporte/', login_required(ListaReporte.as_view()), name='lista-reporte'),
]
