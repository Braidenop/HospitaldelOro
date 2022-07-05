from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.generic import TemplateView, FormView, ListView, CreateView, UpdateView, DeleteView
from medico.forms import RegistroMedicoForm, RegistroUsuarioForm, FormularioLogin, HistoriaForm
from citas.models import Usuario, Medico, Cita, Paciente, Especialidad_Medico, Historiaclinica, Especialidad
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import permission_required
from Intentocitas.mixins import PermisosMedicos
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

from reportes.forms import ReportForm


class homeMedico(LoginRequiredMixin, PermisosMedicos, TemplateView):
    template_name = 'medico/homeMedico.html'


class perfilMedico(TemplateView):
    models = Medico, Especialidad_Medico, Especialidad
    template_name = 'medico/perfilmedico.html'

    # Se envía el contexto que se renderizará en las etiquetas creadas.
    def get_context_data(self, **kwargs):
        context = super(perfilMedico, self).get_context_data(**kwargs)
        medi = Medico.objects.filter(usuario_id=self.request.user.id).values()

        # Se utiliza un values_list para encontrar el campo específico del modelo
        # el flat = True permite traerlo directamente sin los ('')

        esp = Especialidad_Medico.objects.filter(id_medico__usuario_id=self.request.user.id)\
            .values_list('id_especialidad__nombre_esp', flat=True).distinct()
        context['medi'] = medi
        context['esp'] = esp
        return context


class RegistroMedico(TemplateView):
    template_name = 'medico/registroMedi.html'

    def get_context_data(self, **kwargs):
        context = super(RegistroMedico, self).get_context_data(**kwargs)
        context['usuarioForm'] = RegistroUsuarioForm()
        context['medicoForm'] = RegistroMedicoForm()
        return context

    def post(self, request, *args, **kwargs):
        usuario = RegistroUsuarioForm(request.POST)
        medico = RegistroMedicoForm(request.POST, request.FILES)
        if usuario.is_valid() and medico.is_valid():
            Usuario.objects.create_user(username=usuario.cleaned_data['username'],
                                        email=usuario.cleaned_data['email'],
                                        password=usuario.cleaned_data['password']
                                        )
            # Se crea un objeto Usuario con el Usuario recien guardado
            usuario = Usuario.objects.get(username=usuario.cleaned_data['username'])
            medico = medico.save(commit=False)
            medico.usuario = usuario
            medico.save()

            return redirect('medico:login_medico')
        else:
            context = super(RegistroMedico, self).get_context_data(**kwargs)
            context['usuarioForm'] = usuario
            context['medicoForm'] = medico
            return render(request, 'medico/registroMedi.html', context)


class LogoutView(auth_views.LogoutView):
    next_page = '/'


class ListaCita(LoginRequiredMixin, PermisosMedicos, ListView):
    model = Cita
    template_name = 'medico/lista_citas.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_report':
                data = []
                start_date = request.POST.get('start_date', '')
                end_date = request.POST.get('end_date', '')
                search = Cita.objects.all()
                if len(start_date) and len(end_date):
                    search = search.filter(fecha_cita__range=[start_date, end_date],
                                           esp_medic__id_medico__usuario=self.request.user)
                for s in search:
                    data.append(
                        s.toJSON())

            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Citas'
        context['entity'] = 'Listas Citas'
        context['form'] = ReportForm()
        return context


# Consulta

# Cita

class HistoriaList(LoginRequiredMixin, PermisosMedicos, ListView):
    model = Historiaclinica
    template_name = 'medico/listhistoriaclinica.html'
    permission_required = 'view_historiaclinica'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Consultas'
        context['create_url'] = reverse_lazy('medico:crear_hist')
        context['list_url'] = reverse_lazy('medico:lista_hist')
        context['entity'] = 'Listas'
        return context


def hist_crear(request):
    if request.method == "POST":
        form = HistoriaForm(request.POST, request=request)
        if form.is_valid():
            form.save()
            return redirect('medico:lista_hist')
    else:
        form = HistoriaForm(request=request)
    return render(request, 'medico/crear_historia.html', {'form': form,
                                                          'title': 'Creación de Consulta',
                                                          'list_url': reverse_lazy('medico:lista_hist'), })


class EditarHist(LoginRequiredMixin, PermisosMedicos, UpdateView):
    model = Historiaclinica
    template_name = 'medico/crear_historia.html'
    fields = ['id_cita', 'diagnostico', 'examen', 'receta']
    success_url = reverse_lazy('medico:lista_hist')
    url_redirect = success_url
    permission_required = 'change_historiaclinica'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EditarHist, self).get_context_data(**kwargs)
        context['title'] = 'Edición de Historia Clinica'
        context['list_url'] = reverse_lazy('medico:lista_hist')
        context['action'] = 'edit'
        return context


class EliminarHist(LoginRequiredMixin, PermisosMedicos, DeleteView):
    model = Historiaclinica
    template_name = 'medico/deletehist.html'
    success_url = reverse_lazy('medico:lista_hist')
    url_redirect = success_url
    permission_required = 'delete_historiaclinica'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EliminarHist, self).get_context_data(**kwargs)
        context['title'] = 'Eliminación de Historia Clínica'
        context['list_url'] = reverse_lazy('medico:lista_hist')
        context['action'] = 'delete'
        return context


class RecetaPDF(LoginRequiredMixin, PermisosMedicos, View):
    def get(self, request, *args, **kwargs):
        try:
            template = get_template('medico/receta_pdf.html')
            context = {
                'hist': Historiaclinica.objects.get(pk=self.kwargs['pk']),
                'comp': {'name': 'Hospital Básico del Oro', 'ruc': '0999999999998', 'address': 'El Oro'}
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            pisa_status = pisa.CreatePDF(
                html, dest=response)
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('medico:lista_hist'))
