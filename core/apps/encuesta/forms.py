from django import forms
from django.db.models import fields
from django.forms import (ModelForm, inlineformset_factory,
                          modelformset_factory, widgets)
from django.forms.formsets import formset_factory

from .models import Respuesta, Encuesta, Opcion, Tag


class EncuestaForm(ModelForm):
    tag = forms.ModelChoiceField(required=False,
                                 queryset=Tag.objects.filter().order_by('nombre'),
                                 widget=forms.Select(attrs={'class': 'form-control', },
                                                     ))

    class Meta:
        model = Encuesta
        fields = ['pregunta', 'vence', 'tag']

        widgets = {
            'pregunta': forms.TextInput(attrs={'class': "form-control",
                                               'placeholder': "Ingrese consulta...",
                                               'autocomplete': "off"}),
            'vence': forms.DateInput(attrs={'class': "form-control",
                                            'placeholder': "Ingrese fecha...",
                                            'autocomplete': "off"}),
            'tag': forms.Select(attrs={'placeholder': "Ingrese tag...",
                                       'autocomplete': "off", }),
        }


class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['nombre', ]

        widgets = {
            'nombre': forms.TextInput(attrs={'class': "form-control",
                                             'placeholder': "Ingrese nombre...",
                                             'autocomplete': "off"}),
        }


class OpcionForm(ModelForm):
    titulo = forms.CharField(required=False,
                             widget=forms.TextInput(
                                 attrs={'class': 'form-control',
                                        'placeholder': "Ingrese opción...",
                                        'autocomplete': "off"},
                             ))

    class Meta:
        model = Opcion
        fields = ['titulo', ]
        labels = {'titulo': 'Opcion', }


class RespuestaForm(ModelForm):
    # opciones = forms.ModelChoiceField(required=False,
    #                                   widget=forms.Select(attrs={'class': 'form-control', 'placeholder': "Ingrese tag...",
    #                                                              'autocomplete': "off", },
    #                                                       ))

    class Meta:
        model = Respuesta
        fields = ['opcion']
        widgets = {
            'opcion': forms.Select(attrs={'class': 'form-control border-left-primary',
                                          'placeholder': "Ingrese tag...",
                                          'autocomplete': "off", }),
        }
