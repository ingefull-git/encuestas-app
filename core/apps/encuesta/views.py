from os.path import isdir
from django.contrib.auth.models import User
from django.db.models.aggregates import Count, Sum
from django.forms import modelformset_factory
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView)

from .forms import EncuestaForm, OpcionForm, TagForm, RespuestaForm
from .models import Respuesta, Encuesta, Opcion, Tag

# Create your views here.


class ListaEncuesta(ListView):
    model = Encuesta
    template_name = "listado.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ListaEncuesta, self).get_context_data(**kwargs)
        preguntas = Encuesta.objects.all().order_by('vence')
        context['preguntas'] = preguntas
        return context


def nuevaEncuesta(request):
    form = EncuestaForm()
    OpcionFormSet = modelformset_factory(
        Opcion, form=OpcionForm, max_num=4, min_num=1, extra=3)
    formset = OpcionFormSet(queryset=Opcion.objects.none())
    context = {}
    if request.method == 'POST':
        formset = OpcionFormSet(request.POST)
        form = EncuestaForm(request.POST)
        if form.is_valid() and formset.is_valid():
            enc = form.save(commit=False)
            enc.usuario = request.user
            enc = form.save()
            for fset in formset:
                if fset['titulo'].value():
                    opc = fset.save(commit=False)
                    opc.encuesta = enc
                    opc.save()
            return redirect('/')
    context['form'] = form
    context['formset'] = formset
    return render(request, 'nueva.html', context)


def modificaEncuesta(request, pk):
    context = {}
    OpcionFormset = modelformset_factory(
        Opcion, form=OpcionForm, max_num=4, min_num=1, extra=3)
    encuesta = Encuesta.objects.get(id=pk)
    opciones = Opcion.objects.filter(encuesta=encuesta.id)
    form = EncuestaForm(instance=encuesta)
    formset = OpcionFormset(queryset=opciones)
    if request.method == 'POST':
        form = EncuestaForm(request.POST, instance=encuesta)
        formset = OpcionFormset(request.POST, queryset=opciones)
        if form.is_valid():
            if formset.is_valid():
                form.save()
                opcs = formset.save(commit=False)
                for op in opcs:
                    op.encuesta_id = encuesta.id
                    op.save()
                return redirect('/')
    context['formset'] = formset
    context['form'] = form
    return render(request, 'editar.html', context)


def nuevaRespuesta(request, pk):
    context = {}
    encuesta = Encuesta.objects.get(id=pk)
    opciones = Opcion.objects.filter(encuesta=encuesta.id)
    form = RespuestaForm()
    form.fields['opcion'].queryset = opciones
    if request.method == 'POST':
        form = RespuestaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context['encuesta'] = encuesta
    context['opciones'] = opciones
    context['form'] = form
    return render(request, 'responder.html', context)


class ResuladoEncuesta(DetailView):
    model = Encuesta
    template_name = 'resultados.html'

    def get_context_data(self, **kwargs):
        context = super(ResuladoEncuesta, self).get_context_data(**kwargs)
        encuesta = kwargs['object']
        opciones = Opcion.objects.filter(encuesta=encuesta.id)
        respuestas = Opcion.objects.filter(
            encuesta_id=encuesta.id).order_by('titulo').annotate(resultado=Count('respuesta'))
        total = Respuesta.objects.filter(
            opcion__encuesta_id=encuesta.id).count()
        context['encuesta'] = encuesta
        context['opciones'] = opciones
        context['respuestas'] = respuestas
        context['total'] = total
        return context


class BorraEncuesta(DeleteView):
    model = Encuesta
    template_name = 'borrar.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pregunta = Encuesta.objects.get(id=self.object.id)
        context['pregunta'] = pregunta
        return context


class ListaTag(ListView):
    model = Tag
    template_name = 'tags_listado.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ListaTag, self).get_context_data(**kwargs)
        tags = Tag.objects.all().order_by('nombre')
        context['tags'] = tags
        return context


class NuevoTag(CreateView):
    model = Tag
    template_name = 'tags_nuevo.html'
    form_class = TagForm
    success_url = reverse_lazy('encuesta:lista-tag')


class BorraTag(DeleteView):
    model = Tag
    template_name = 'tags_borrar.html'
    success_url = '/tag/listado/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = Tag.objects.get(id=self.object.id)
        context['tag'] = tag
        return context


class ListaReporte(ListView):
    model = Encuesta
    template_name = 'reporte_listado.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ListaReporte, self).get_context_data(**kwargs)
        usuarios = User.objects.all().order_by('username')
        tags = Tag.objects.all().order_by('nombre')
        if self.request.method == 'GET':
            preguntas = ""
            try:
                usuario = int(self.request.GET.get('userSel'))
                tag = int(self.request.GET.get('tagSel'))
                if usuario > 0 and tag > 0:
                    preguntas = Encuesta.objects.filter(
                        usuario=usuario, tag=tag).order_by('vence')
                elif usuario > 0 and tag == 0:
                    preguntas = Encuesta.objects.filter(
                        usuario=usuario).order_by('vence')
                elif usuario == 0 and tag > 0:
                    preguntas = Encuesta.objects.filter(
                        tag=tag).order_by('vence')
                else:
                    preguntas = Encuesta.objects.all().order_by('vence')
            except Exception:
                preguntas = Encuesta.objects.all().order_by('vence')
        context['usuarios'] = usuarios
        context['tags'] = tags
        context['preguntas'] = preguntas
        return context
