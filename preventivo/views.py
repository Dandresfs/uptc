from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from .forms import NuevaActividad, PlanMantenimiento
from inventario_equipos.forms import NuevoPlan
from .models import Actividades
from inventario_equipos.models import InventarioEquipos
from .serializers import EventSerializer, EventFullSerializer, ActividadSerializer
from .models import EventCalendar,TipoMantenimiento
from django.views.generic.edit import DeleteView, UpdateView


class PlanView(ListView):
    model = InventarioEquipos
    template_name = "plan.html"

    def get_context_data(self, **kwargs):
        if self.kwargs['tipo'] == '1':
            kwargs['pdf'] = InventarioEquipos.objects.get(id=self.kwargs['idmachine']).preventivo
        if self.kwargs['tipo'] == '2':
            kwargs['pdf'] = InventarioEquipos.objects.get(id=self.kwargs['idmachine']).correctivo
        if self.kwargs['tipo'] == '3':
            kwargs['pdf'] = InventarioEquipos.objects.get(id=self.kwargs['idmachine']).preventivo
        if self.kwargs['tipo'] == '4':
            kwargs['pdf'] = InventarioEquipos.objects.get(id=self.kwargs['idmachine']).rcm
        if self.kwargs['tipo'] == '5':
            kwargs['pdf'] = InventarioEquipos.objects.get(id=self.kwargs['idmachine']).tpm
        kwargs['tipomantenimiento'] = TipoMantenimiento.objects.get(id=self.kwargs['tipo']).nombre
        kwargs['maquina'] = InventarioEquipos.objects.get(id=self.kwargs['idmachine']).nombre
        return super(PlanView,self).get_context_data(**kwargs)

class PlanTipoView(ListView):
    model = TipoMantenimiento
    template_name = "plan_tipo.html"

    def get_context_data(self, **kwargs):
        kwargs['pdf'] = TipoMantenimiento.objects.get(id=self.kwargs['idmantenimiento']).plan
        kwargs['tipomantenimiento'] = TipoMantenimiento.objects.get(id=self.kwargs['idmantenimiento']).nombre
        return super(PlanTipoView,self).get_context_data(**kwargs)

class PlanUpdateView(UpdateView):
    template_name = "plan_actualizar.html"
    model = InventarioEquipos
    form_class = NuevoPlan
    pk_url_kwarg = 'idmachine'
    success_url = "../"

    def get_context_data(self, **kwargs):
        kwargs['tipomantenimiento'] = TipoMantenimiento.objects.get(id=self.kwargs['tipo']).nombre.lower()
        kwargs['maquina'] = InventarioEquipos.objects.get(id=self.kwargs['idmachine']).nombre
        return super(PlanUpdateView,self).get_context_data(**kwargs)

class PlanTipoUpdateView(UpdateView):
    template_name = "plan_tipo_actualizar.html"
    model = TipoMantenimiento
    form_class = PlanMantenimiento
    pk_url_kwarg = 'idmantenimiento'
    success_url = "../"

    def get_context_data(self, **kwargs):
        kwargs['nombremantenimiento'] = TipoMantenimiento.objects.get(id=self.kwargs['idmantenimiento']).nombre
        kwargs['tipomantenimiento'] = TipoMantenimiento.objects.get(id=self.kwargs['idmantenimiento']).nombre.lower()
        return super(PlanTipoUpdateView,self).get_context_data(**kwargs)

class ActividadView(ListView):
    model = Actividades
    template_name = "lista_actividades.html"

    def get_queryset(self):
        queryset = Actividades.objects.all().filter(maquina__id=self.kwargs['idmachine']).filter(tipo__id=self.kwargs['tipo'])
        return queryset

    def get_context_data(self, **kwargs):
        kwargs['nombremaquina'] = InventarioEquipos.objects.get(id=self.kwargs['idmachine']).nombre
        kwargs['colormaquina'] = InventarioEquipos.objects.get(id=self.kwargs['idmachine']).color
        kwargs['tipomantenimiento'] = TipoMantenimiento.objects.get(id=self.kwargs['tipo']).nombre
        return super(ActividadView,self).get_context_data(**kwargs)

class ActividadEditarView(ListView):
    model = Actividades
    template_name = "lista_actividades_editar.html"

    def get_queryset(self):
        queryset = Actividades.objects.all().filter(maquina__id=self.kwargs['idmachine']).filter(tipo__id=self.kwargs['tipo'])
        return queryset

    def get_context_data(self, **kwargs):
        kwargs['nombremaquina'] = InventarioEquipos.objects.get(id=self.kwargs['idmachine']).nombre
        kwargs['tipomantenimiento'] = TipoMantenimiento.objects.get(id=self.kwargs['tipo']).nombre
        kwargs['colormaquina'] = InventarioEquipos.objects.get(id=self.kwargs['idmachine']).color
        return super(ActividadEditarView,self).get_context_data(**kwargs)

class InventarioView(ListView):
    model = InventarioEquipos
    template_name = 'lista_maquinas.html'

    def get_context_data(self, **kwargs):
        kwargs['nombremantenimiento'] = TipoMantenimiento.objects.get(id=self.kwargs['idmantenimiento']).nombre
        return super(InventarioView,self).get_context_data(**kwargs)

class NuevaActividadForm(FormView):
    template_name = 'nueva_actividad.html'
    form_class = NuevaActividad
    success_url = '../../'

    def form_valid(self, form):
        form.instance.maquina = InventarioEquipos.objects.get(pk = self.kwargs['idmachine'])
        form.instance.tipo = TipoMantenimiento.objects.get(pk = self.kwargs['tipo'])
        form.save()
        return super(NuevaActividadForm, self).form_valid(form)

    def get_context_data(self, **kwargs):
        kwargs['nombremantenimiento'] = TipoMantenimiento.objects.get(id=self.kwargs['tipo']).nombre
        kwargs['nombremaquina'] = InventarioEquipos.objects.get(id=self.kwargs['idmachine']).nombre
        kwargs['tipo'] = 'Nueva'
        return super(NuevaActividadForm,self).get_context_data(**kwargs)

class ActividadDeleteView(DeleteView):

    template_name = 'eliminar_actividad.html'
    model = Actividades
    success_url = '../../../'

    def get_success_url(self):
        events = EventCalendar.objects.all().filter(title=Actividades.objects.get(pk=self.kwargs['pk']))
        for event in events:
            event.delete()
        return  super(ActividadDeleteView,self).get_success_url()

    def get_context_data(self, **kwargs):
        kwargs['nombremantenimiento'] = TipoMantenimiento.objects.get(id=self.kwargs['tipo']).nombre
        kwargs['nombremaquina'] = InventarioEquipos.objects.get(id=self.kwargs['idmachine']).nombre
        return super(ActividadDeleteView,self).get_context_data(**kwargs)

class ActividadUpdateView(UpdateView):
    template_name = 'nueva_actividad.html'
    model = Actividades
    form_class = NuevaActividad
    success_url = '../../../'

    def get_context_data(self, **kwargs):
        kwargs['nombremantenimiento'] = TipoMantenimiento.objects.get(id=self.kwargs['tipo']).nombre
        kwargs['nombremaquina'] = InventarioEquipos.objects.get(id=self.kwargs['idmachine']).nombre
        kwargs['tipo'] = 'Editar'
        return super(ActividadUpdateView,self).get_context_data(**kwargs)

class CalendarioView(ListView):
    model = Actividades
    template_name = 'calendario.html'

    def get_queryset(self):
        queryset = Actividades.objects.all().filter(maquina__id=self.kwargs['idmachine']).filter(tipo__id=self.kwargs['idmantenimiento'])
        return queryset

    def get_context_data(self, **kwargs):
        kwargs['color'] = InventarioEquipos.objects.all().filter(id=self.kwargs['idmachine'])[0].color
        kwargs['mantenimiento'] = self.kwargs['idmantenimiento']
        kwargs['nombremantenimiento'] = TipoMantenimiento.objects.get(id=self.kwargs['idmantenimiento']).nombre
        kwargs['maquina'] = self.kwargs['idmachine']
        kwargs['nombremaquina'] = InventarioEquipos.objects.get(id=self.kwargs['idmachine']).nombre
        return super(CalendarioView,self).get_context_data(**kwargs)

class FormatosView(TemplateView):
    template_name = "formatos.html"

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.http import Http404
from rest_framework.permissions import IsAuthenticated

class EventList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, maquina, mantenimiento, format=None):
        snippet = EventCalendar.objects.all().filter(mantenimiento__id=mantenimiento).filter(maquina__id=maquina)
        serializer = EventSerializer(snippet,many=True)
        return Response(serializer.data)

    def post(self, request, maquina, mantenimiento, format=None):
        serializer = EventFullSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventDetail(APIView):

    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return EventCalendar.objects.get(pk=pk)
        except EventCalendar.DoesNotExist:
            raise Http404

    def get(self, request, pk, maquina, mantenimiento, format=None):
        snippet = self.get_object(pk)
        serializer = EventSerializer(snippet)
        return Response(serializer.data)


    def put(self, request, pk, maquina, mantenimiento ,format=None):
        snippet = self.get_object(pk)
        serializer = EventSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, maquina, mantenimiento, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class EventListMachine(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, maquina, format=None):
        snippet = EventCalendar.objects.all().filter(maquina__id=maquina)
        serializer = EventSerializer(snippet,many=True)
        return Response(serializer.data)

class EventListFull(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        snippet = EventCalendar.objects.all()
        serializer = EventSerializer(snippet,many=True)
        return Response(serializer.data)

class EventListMantenimiento(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, mantenimiento, format=None):
        snippet = EventCalendar.objects.all().filter(mantenimiento__id=mantenimiento)
        serializer = EventSerializer(snippet,many=True)
        return Response(serializer.data)

class ActividadList(APIView):
    permission_classes = (IsAuthenticated,)



    def get(self, request, nombre, format=None):
        snippet = Actividades.objects.all().filter(nombre=nombre)
        serializer = ActividadSerializer(snippet,many=True)
        return Response(serializer.data)