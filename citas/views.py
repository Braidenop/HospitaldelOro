from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.checks import messages
from django.http import HttpResponseRedirect, request, JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from reportes.forms import ReportForm
from .forms import FormularioLogin, TestFormPac
from .models import Usuario, Paciente, Cita, Consulta, Especialidad_Medico, Especialidad
from .forms import RegistroUsuarioForm, RegistroPacienteForm
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.contrib.auth.models import Group


# Vista para la plantilla base
class homePaciente(TemplateView):
    template_name = 'homePaciente.html'


# Vista para la página de Información
class Info(TemplateView):
    template_name = 'info.html'


# Vista para la página de Servicios
class Services(TemplateView):
    template_name = 'Services.html'


# Vista para la página de Contacto
class Contacto(TemplateView):
    template_name = 'contacto.html'


# Vista para la página de Perfil
class Perfil(TemplateView):
    model = Paciente
    template_name = 'perfil.html'

    # Se envía el contexto que se renderizará en las etiquetas creadas.
    def get_context_data(self, **kwargs):
        context = super(Perfil, self).get_context_data(**kwargs)
        paci = Paciente.objects.filter(usuario_id=self.request.user.id).values()
        context['paci'] = paci

        return context


# Vista para la página de Registro
class Registro(TemplateView):
    template_name = 'registro.html'

    # Se envía el contexto que se renderizará en las etiquetas creadas.
    def get_context_data(self, **kwargs):
        context = super(Registro, self).get_context_data(**kwargs)
        context['usuarioForm'] = RegistroUsuarioForm()
        context['pacienteForm'] = RegistroPacienteForm()
        return context

    # Método Post para enviar la información de los dos formularios y crear
    # un objeto Usuario - Paciente
    def post(self, request, *args, **kwargs):
        usuario = RegistroUsuarioForm(request.POST, request.FILES)
        paciente = RegistroPacienteForm(request.POST)
        if usuario.is_valid() and paciente.is_valid():
            Usuario.objects.create_user(username=usuario.cleaned_data['username'],
                                        email=usuario.cleaned_data['email'],
                                        password=usuario.cleaned_data['password'],
                                        first_name=usuario.cleaned_data['first_name'],
                                        last_name=usuario.cleaned_data['last_name'],
                                        image=usuario.cleaned_data['image'],
                                        )
            # Se crea un objeto Usuario con el Usuario recien guardado
            usuario = Usuario.objects.get(username=usuario.cleaned_data['username'])
            paciente = paciente.save(commit=False)
            paciente.usuario = usuario
            paciente.save()
            group = Group.objects.get(name='Paciente')
            group.user_set.add(usuario)

            return redirect('citas:login')
        else:
            context = super(Registro, self).get_context_data(**kwargs)
            context['usuarioForm'] = usuario
            context['pacienteForm'] = paciente
            return render(request, 'registro.html', context)


# Vista - Método para ingresar al sistema
def login_user(request):
    if request.method == 'POST':
        form = FormularioLogin(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if request.user.groups.filter(name='Medico').exists():
                    return redirect('medico:home_medico')
                else:
                    if request.user.groups.filter(name='Paciente').exists():
                        return redirect('citas:homePaciente')
                    else:
                        if request.user.groups.filter(name='Administrador').exists():
                            return redirect('admi:home')
                        else:
                            if request.user.groups.filter(name='Secretaria').exists():
                                return redirect('admi:home')
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'login.html', context={'form': FormularioLogin()})


# Vista para mostrar la lista de Citas Agendadas.
class AgendaCita(LoginRequiredMixin, ListView):
    model = Cita
    template_name = 'ListaCItas.html'

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
                                           paciente=self.request.user)
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
        context['create_url'] = reverse_lazy('citas:crear_cita')
        context['list_url'] = reverse_lazy('citas:lista_citas')
        context['entity'] = 'Listas'
        context['form'] = ReportForm()
        actualcita = Consulta.objects.all().filter(id_cita__paciente=self.request.user, id_cita__esp_medic__fecha_cita=datetime.today())
        context['actual'] = actualcita
        return context


# Vista para crear una Cita
class CrearCita(LoginRequiredMixin, CreateView):
    model = Cita
    template_name = 'crearCita.html'
    fields = ['esp_medic', 'motivo']
    success_url = reverse_lazy('citas:lista_citas')
    url_redirect = success_url

    def get_queryset(self):
        return Cita.objects.filter(paciente=self.request.user)

    def form_valid(self, form):
        form.instance.paciente = self.request.user
        self.object = form.save
        return super(CrearCita, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CrearCita, self).get_context_data(**kwargs)
        context['title'] = 'Agendamiento de Cita'
        context['entity'] = 'Citas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['especialidad'] = Especialidad.objects.all()
        context['medico'] = Especialidad_Medico.objects.all()
        context['horario'] = Especialidad_Medico.objects.all()
        return context


# Vista para editar una Cita
class EditarCita(LoginRequiredMixin, UpdateView):
    model = Cita
    template_name = 'crearCita.html'
    fields = ['esp_medic', 'motivo']
    success_url = reverse_lazy('citas:lista_citas')
    url_redirect = success_url

    def get_queryset(self):
        return Cita.objects.filter(paciente=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(EditarCita, self).get_context_data(**kwargs)
        context['title'] = 'Agendamiento de Cita'
        context['entity'] = 'Citas'
        context['list_url'] = self.success_url
        context['action'] = 'change'
        return context

    def form_valid(self, form):
        form.instance.paciente = self.request.user
        self.object = form.save
        return super(EditarCita, self).form_valid(form)


# Vista para eliminar una Cita
class EliminarCita(LoginRequiredMixin, DeleteView):
    model = Cita
    template_name = 'eliminarCita.html'
    success_url = reverse_lazy('citas:lista_citas')
    url_redirect = success_url

    def get_context_data(self, **kwargs):
        context = super(EliminarCita, self).get_context_data(**kwargs)
        context['title'] = 'Agendamiento de Cita'
        context['entity'] = 'Citas'
        context['list_url'] = self.success_url
        context['action'] = 'delete'
        return context


class CalendarioCitas(LoginRequiredMixin, ListView):
    model = Cita
    template_name = 'calendisp.html'

    def get_queryset(self):
        queryset = Cita.objects.all()
        return queryset


class LogoutView(auth_views.LogoutView):
    next_page = '/'


class TestForm(CreateView):
    model = Cita
    template_name = 'test.html'
    form_class = TestFormPac
    success_url = reverse_lazy('citas:lista_citas')
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super(TestForm, self).get_context_data(**kwargs)
        context['title'] = 'Prueba de Agendamiento'
        context['entity'] = 'Citas'
        context['action'] = 'test'
        context['list_url'] = reverse_lazy('citas:lista_citas')
        context['form'] = TestFormPac()
        context['especialidad'] = Especialidad.objects.all()
        context['medico'] = Especialidad_Medico.objects.all()
        context['horario'] = Especialidad_Medico.objects.all()
        return context
