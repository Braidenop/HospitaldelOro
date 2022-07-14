from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView
from medico.forms import RegistroMedicoForm, RegistroUsuarioForm, ConsultaForm
from citas.models import Usuario, Medico, Cita, Especialidad_Medico, Consulta, Especialidad
from django.contrib.auth import views as auth_views
from Intentocitas.mixins import PermisosMedicos
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
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

        esp = Especialidad_Medico.objects.filter(id_medico__usuario_id=self.request.user.id) \
            .values_list('id_especialidad__nombre_esp', flat=True).distinct()
        context['medi'] = medi
        context['esp'] = esp
        return context


# Vista para el Registro
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


# Vista para Citas Agendadas
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
                    search = search.filter(esp_medic__fecha_cita__range=[start_date, end_date],
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


#  Lista de Consultas

class ConsultaList(LoginRequiredMixin, PermisosMedicos, ListView):
    model = Consulta
    template_name = 'medico/listconsul.html'
    permission_required = 'view_consulta'

    def get_queryset(self):
        queryset = Consulta.objects.select_related().filter(id_cita__esp_medic__id_medico__usuario=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Consultas'
        context['create_url'] = reverse_lazy('medico:crear_consul')
        context['list_url'] = reverse_lazy('medico:lista_consul')
        context['entity'] = 'Listas'
        return context


# Crear una Consulta

def consul_crear(request):
    if request.method == "POST":
        form = ConsultaForm(request.POST, request=request)
        if form.is_valid():
            form.save()
            return redirect('medico:lista_consul')
    else:
        form = ConsultaForm(request=request)
    return render(request, 'medico/crear_consulta.html', {'form': form,
                                                          'title': 'Creación de Consulta',
                                                          'list_url': reverse_lazy('medico:lista_consul'), })


# Editar una Consulta
class EditarConsul(LoginRequiredMixin, PermisosMedicos, UpdateView):
    model = Consulta
    template_name = 'medico/crear_consulta.html'
    fields = ['id_cita', 'diagnostico', 'examen', 'receta']
    success_url = reverse_lazy('medico:lista_consul')
    url_redirect = success_url
    permission_required = 'change_consulta'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EditarConsul, self).get_context_data(**kwargs)
        context['title'] = 'Edición de Historia Clinica'
        context['list_url'] = reverse_lazy('medico:lista_consul')
        context['action'] = 'edit'
        return context


# Eliminar una consulta
class EliminarConsul(LoginRequiredMixin, PermisosMedicos, DeleteView):
    model = Consulta
    template_name = 'medico/deleteconsul.html'
    success_url = reverse_lazy('medico:lista_consul')
    url_redirect = success_url
    permission_required = 'delete_consulta'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EliminarConsul, self).get_context_data(**kwargs)
        context['title'] = 'Eliminación de Consulta'
        context['list_url'] = reverse_lazy('medico:lista_consul')
        context['action'] = 'delete'
        return context


# Crear PDF de Receta
class RecetaPDF(LoginRequiredMixin, PermisosMedicos, View):
    def get(self, request, *args, **kwargs):
        try:
            template = get_template('medico/receta_pdf.html')
            context = {
                'hist': Consulta.objects.get(pk=self.kwargs['pk']),
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
        return HttpResponseRedirect(reverse_lazy('medico:lista_consul'))
