from datetime import datetime
from django.contrib.auth import views as auth_views

from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from citas.forms import RegistroUsuarioForm, RegistroPacienteForm
from citas.models import Usuario, Especialidad, Medico, Especialidad_Medico, Cita, Examen, Receta, Medicamento, \
    Paciente, Consulta
from medico.forms import RegistroMedicoForm
from reportes.forms import ReportForm
from .forms import CrearUsuarioForm, EspecialidadForm, MedicoForm, DisponibilidadForm, CitaForm, \
    MedicamentoForm, ExamenForm, RecetaForm, EditarUsuarioForm, PacienteForm
from Intentocitas.mixins import PermisosGrupos


# Vista para página de Administrador
class homeAdmin(LoginRequiredMixin, PermisosGrupos, TemplateView):
    template_name = 'admi/homeAdmi.html'

    def get_graph_sales_year_month(self):
        data = []
        try:
            year = datetime.now().year
            for m in range(1, 13):
                total = Cita.objects.filter(esp_medic__fecha_cita__year=year, esp_medic__fecha_cita__month=m).count()
                data.append((total))
        except:
            pass
        return data


    def total_consul_inf(self):
        tot_consul = Consulta.objects.all().count()
        tot_enf_inf = Consulta.objects.filter(tipo_enf='Infecciosa o Parasitaria').count()
        porc_enf_inf = int((tot_enf_inf * 100) / tot_consul)
        return porc_enf_inf

    def total_consul_endo(self):
        tot_consul = Consulta.objects.all().count()
        tot_enf_end = Consulta.objects.filter(tipo_enf='Endocrina').count()
        porc_enf_end = int((tot_enf_end * 100) / tot_consul)
        return porc_enf_end

    def total_consul_resp(self):
        tot_consul = Consulta.objects.all().count()
        tot_enf_resp = Consulta.objects.filter(tipo_enf='Respiratoria').count()
        porc_enf_resp = int((tot_enf_resp * 100) / tot_consul)
        return porc_enf_resp

    def total_consul_neu(self):
        tot_consul = Consulta.objects.all().count()
        tot_enf_neu = Consulta.objects.filter(tipo_enf='Neuronal').count()
        porc_enf_neu = int((tot_enf_neu * 100) / tot_consul)
        return porc_enf_neu


    def total_consul_gas(self):
        tot_consul = Consulta.objects.all().count()
        tot_enf_gas = Consulta.objects.filter(tipo_enf='Gastrica').count()
        porc_enf_gas = int((tot_enf_gas * 100) / tot_consul)
        return porc_enf_gas

    def count_medico(self):
        data = []
        try:
            espe = Especialidad.objects.values_list('nombre_esp', flat=True)

            for m in espe:
                med = Medico.objects.filter(esp__nombre_esp=m).distinct().count()
                data.append((med))
        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['panel'] = 'Panel de administrador'
        context['graph_sales_year_month'] = self.get_graph_sales_year_month()
        context['count_medico'] = self.count_medico()
        esp = Especialidad.objects.all()
        context['esp'] = esp
        context['pac'] = Paciente.objects.count()
        context['med'] = Medico.objects.count()
        context['espci'] = Especialidad.objects.count()
        context['consul'] = Consulta.objects.filter(tipo_enf='Respiratoria')
        context['tot_enf_inf'] = self.total_consul_inf()
        context['tot_enf_endo'] = self.total_consul_endo()
        context['tot_enf_resp'] = self.total_consul_resp()
        context['tot_enf_gas'] = self.total_consul_gas()
        context['tot_enf_neu'] = self.total_consul_neu()

        return context


#  Usuario
class listUsuarios(LoginRequiredMixin, PermisosGrupos, ListView):
    model = Usuario
    template_name = 'admi/user/list_usuarios.html'
    permission_required = 'view_usuario'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Usuario.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Usuarios'
        context['create_url'] = reverse_lazy('admi:crear_usuario')
        context['list_url'] = reverse_lazy('admi:lista_usuarios')
        context['entity'] = 'Usuarios'
        return context


class crearUsuario(LoginRequiredMixin, PermisosGrupos, CreateView):
    model = Usuario
    template_name = 'admi/user/crear_usuario.html'
    form_class = CrearUsuarioForm
    success_url = reverse_lazy('admi:lista_usuarios')
    permission_required = 'add_usuario'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de un Usuario'
        context['entity'] = 'Usuarios'
        context['list_url'] = reverse_lazy('admi:lista_usuarios')
        context['action'] = 'add'
        return context


class editarUsuario(LoginRequiredMixin, PermisosGrupos, UpdateView):
    model = Usuario
    template_name = 'admi/user/crear_usuario.html'
    form_class = EditarUsuarioForm
    success_url = reverse_lazy('admi:lista_usuarios')
    permission_required = 'change_usuario'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de un Usuario'
        context['entity'] = 'Usuarios'
        context['list_url'] = reverse_lazy('admi:lista_usuarios')
        context['action'] = 'edit'
        return context


class eliminarUsuario(LoginRequiredMixin, PermisosGrupos, DeleteView):
    model = Usuario
    template_name = 'admi/user/delete_user.html'
    success_url = reverse_lazy('admi:lista_usuarios')
    permission_required = 'delete_usuario'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un usuario'
        context['entity'] = 'Usuarios'
        context['list_url'] = reverse_lazy('admi:lista_usuarios')
        context['action'] = 'delete'
        return context


# Paciente
class listPacientes(LoginRequiredMixin, PermisosGrupos, ListView):
    model = Paciente
    template_name = 'admi/paciente/list_pacientes.html'
    permission_required = 'view_paciente'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Paciente.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Pacientes'
        context['create_url'] = reverse_lazy('admi:crear_pacie')
        context['list_url'] = reverse_lazy('admi:lista_pacie')
        context['entity'] = 'Pacientes'
        return context


class crearPaciente(LoginRequiredMixin, PermisosGrupos, TemplateView):
    template_name = 'admi/paciente/crear_paciente.html'
    permission_required = 'add_paciente'

    def get_context_data(self, **kwargs):
        context = super(crearPaciente, self).get_context_data(**kwargs)
        context['usuarioForm'] = RegistroUsuarioForm()
        context['pacienteForm'] = RegistroPacienteForm()
        context['title'] = 'Creación de un Paciente'
        context['entity'] = 'Pacientes'
        context['list_url'] = reverse_lazy('admi:lista_pacie')
        context['action'] = 'add'
        return context

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

            return redirect('admi:lista_pacie')
        else:
            context = super(crearPaciente, self).get_context_data(**kwargs)
            context['usuarioForm'] = usuario
            context['pacienteForm'] = paciente
            return render(request, 'admi/paciente/crear_paciente.html', context)


class editarPaciente(LoginRequiredMixin, PermisosGrupos, UpdateView):
    model = Paciente
    template_name = 'admi/paciente/editar_paciente.html'
    form_class = PacienteForm
    success_url = reverse_lazy('admi:lista_pacie')
    permission_required = 'change_paciente'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de datos de Paciente'
        context['entity'] = 'Pacientes'
        context['list_url'] = reverse_lazy('admi:lista_pacie')
        context['action'] = 'edit'
        return context


class eliminarPaciente(LoginRequiredMixin, PermisosGrupos, DeleteView):
    model = Paciente
    template_name = 'admi/paciente/delete_pacient.html'
    success_url = reverse_lazy('admi:lista_pacie')
    permission_required = 'delete_paciente'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un Paciente'
        context['entity'] = 'Pacientes'
        context['list_url'] = reverse_lazy('admi:lista_pacie')
        context['action'] = 'delete'
        return context


# Especialidad

class listEspe(LoginRequiredMixin, PermisosGrupos, ListView):
    model = Especialidad
    template_name = 'admi/especialidad/lista_espe.html'
    permission_required = 'view_especialidad'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Especialidad.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Especialidades'
        context['create_url'] = reverse_lazy('admi:crear_espe')
        context['list_url'] = reverse_lazy('admi:lista_espe')
        context['entity'] = 'Especialidades'
        return context


class crearEspe(LoginRequiredMixin, PermisosGrupos, CreateView):
    model = Especialidad
    template_name = 'admi/especialidad/crear_especialidad.html'
    form_class = EspecialidadForm
    success_url = reverse_lazy('admi:lista_espe')
    permission_required = 'add_especialidad'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de una Especialidad'
        context['entity'] = 'Especialidades'
        context['list_url'] = reverse_lazy('admi:lista_espe')
        context['action'] = 'add'
        return context


class editarEspe(LoginRequiredMixin, PermisosGrupos, UpdateView):
    model = Especialidad
    template_name = 'admi/especialidad/crear_especialidad.html'
    form_class = EspecialidadForm
    success_url = reverse_lazy('admi:lista_espe')
    permission_required = 'change_especialidad'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de una Especialidad'
        context['entity'] = 'Especialidades'
        context['list_url'] = reverse_lazy('admi:lista_espe')
        context['action'] = 'edit'
        return context


class eliminarEspe(LoginRequiredMixin, PermisosGrupos, DeleteView):
    model = Especialidad
    template_name = 'admi/especialidad/delete_espe.html'
    success_url = reverse_lazy('admi:lista_espe')
    permission_required = 'delete_especialidad'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de una Especialidad'
        context['entity'] = 'Especialidades'
        context['list_url'] = reverse_lazy('admi:lista_espe')
        context['action'] = 'delete'
        return context


# Medicos

class listMedi(LoginRequiredMixin, PermisosGrupos, ListView):
    model = Medico
    template_name = 'admi/medico/list_medicos.html'
    permission_required = 'view_medico'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Medico.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Médicos'
        context['create_url'] = reverse_lazy('admi:crear_medi')
        context['list_url'] = reverse_lazy('admi:lista_medi')
        context['entity'] = 'Medicos'
        return context


class crearMedi(LoginRequiredMixin, PermisosGrupos, TemplateView):
    template_name = 'admi/medico/crear_medico.html'
    permission_required = 'add_medico'

    def get_context_data(self, **kwargs):
        context = super(crearMedi, self).get_context_data(**kwargs)
        context['usuarioForm'] = RegistroUsuarioForm()
        context['medicoForm'] = RegistroMedicoForm()
        context['title'] = 'Creación de un Medico'
        context['entity'] = 'Medicos'
        context['list_url'] = reverse_lazy('admi:lista_medi')
        context['action'] = 'add'
        return context

    def post(self, request, *args, **kwargs):
        usuario = RegistroUsuarioForm(request.POST, request.FILES)
        medico = RegistroMedicoForm(request.POST)
        if usuario.is_valid() and medico.is_valid():
            Usuario.objects.create_user(username=usuario.cleaned_data['username'],
                                        email=usuario.cleaned_data['email'],
                                        password=usuario.cleaned_data['password'],
                                        first_name=usuario.cleaned_data['first_name'],
                                        last_name=usuario.cleaned_data['last_name'],
                                        image=usuario.cleaned_data['image'],
                                        )
            # Se crea un objeto Usuario con el Usuario recien guardado
            usuario = Usuario.objects.get(username=usuario.cleaned_data['username'])
            medico = medico.save(commit=False)
            medico.usuario = usuario
            medico.save()
            group = Group.objects.get(name='Medico')
            group.user_set.add(usuario)

            return redirect('admi:lista_medi')
        else:
            context = super(crearMedi, self).get_context_data(**kwargs)
            context['usuarioForm'] = usuario
            context['medicoForm'] = medico
            return render(request, 'admi/medico/crear_medico.html', context)


class editarMedi(LoginRequiredMixin, PermisosGrupos, UpdateView):
    model = Medico
    template_name = 'admi/medico/editar_medico.html'
    form_class = MedicoForm
    success_url = reverse_lazy('admi:lista_medi')
    permission_required = 'change_medico'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de datos de Medico'
        context['entity'] = 'Medicos'
        context['list_url'] = reverse_lazy('admi:lista_medi')
        context['action'] = 'edit'
        return context


class eliminarMedi(LoginRequiredMixin, PermisosGrupos, DeleteView):
    model = Medico
    template_name = 'admi/medico/delete_medico.html'
    success_url = reverse_lazy('admi:lista_medi')
    permission_required = 'delete_medico'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un Medico'
        context['entity'] = 'Medicos'
        context['list_url'] = reverse_lazy('admi:lista_medi')
        context['action'] = 'delete'
        return context


# Disponibilidad

class listDispo(LoginRequiredMixin, PermisosGrupos, ListView):
    model = Especialidad_Medico
    template_name = 'admi/disponiblidad/list_dispo.html'
    permission_required = 'view_especialidad_medico'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Especialidad_Medico.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Disponibilidad de Horario'
        context['create_url'] = reverse_lazy('admi:crear_dipo')
        context['list_url'] = reverse_lazy('admi:lista_dipo')
        context['entity'] = 'Disponibilidad'
        return context


class crearDispo(LoginRequiredMixin, PermisosGrupos, CreateView):
    model = Especialidad_Medico
    template_name = 'admi/disponiblidad/crear_dispo.html'
    form_class = DisponibilidadForm
    success_url = reverse_lazy('admi:lista_dipo')
    permission_required = 'add_especialidad_medico'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Escoja la disponibilidad de Horario'
        context['entity'] = 'Disponibilidad'
        context['list_url'] = reverse_lazy('admi:lista_dipo')
        context['action'] = 'add'
        return context


class editarDispo(LoginRequiredMixin, PermisosGrupos, UpdateView):
    model = Especialidad_Medico
    template_name = 'admi/disponiblidad/crear_dispo.html'
    form_class = DisponibilidadForm
    success_url = reverse_lazy('admi:lista_dipo')
    permission_required = 'change_especialidad_medico'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de datos de la disponibilidad de Horario'
        context['entity'] = 'Disponibilidad'
        context['list_url'] = reverse_lazy('admi:lista_dipo')
        context['action'] = 'edit'
        return context


class eliminarDispo(LoginRequiredMixin, PermisosGrupos, DeleteView):
    model = Especialidad_Medico
    template_name = 'admi/disponiblidad/delete_dispo.html'
    success_url = reverse_lazy('admi:lista_dipo')
    permission_required = 'delete_especialidad_medico'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un Horario'
        context['entity'] = 'Disponibilidad'
        context['list_url'] = reverse_lazy('admi:lista_dipo')
        context['action'] = 'delete'
        return context


# Cita

class AgendaCita(LoginRequiredMixin, PermisosGrupos, ListView):
    model = Cita
    template_name = 'admi/cita/list_cita.html'
    permission_required = 'view_cita'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Cita.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Citas'
        context['create_url'] = reverse_lazy('admi:crear_cita')
        context['list_url'] = reverse_lazy('admi:lista_cita')
        context['entity'] = 'Listas'
        return context


class CrearCita(LoginRequiredMixin, PermisosGrupos, CreateView):
    model = Cita
    template_name = 'admi/cita/crear_cita.html'
    form_class = CitaForm
    success_url = reverse_lazy('admi:lista_cita')
    url_redirect = success_url
    permission_required = 'add_cita'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CrearCita, self).get_context_data(**kwargs)
        context['title'] = 'Agendamiento de Cita'
        context['entity'] = 'Citas'
        context['list_url'] = reverse_lazy('admi:lista_cita')
        context['action'] = 'add'
        return context


class EditarCita(LoginRequiredMixin, PermisosGrupos, UpdateView):
    model = Cita
    template_name = 'admi/cita/crear_cita.html'
    form_class = CitaForm
    success_url = reverse_lazy('citas:lista_citas')
    url_redirect = success_url
    permission_required = 'change_cita'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EditarCita, self).get_context_data(**kwargs)
        context['title'] = 'Cambio de Cita'
        context['entity'] = 'Citas'
        context['list_url'] = reverse_lazy('admi:lista_cita')
        context['action'] = 'change'
        return context


class EliminarCita(LoginRequiredMixin, PermisosGrupos, DeleteView):
    model = Cita
    template_name = 'admi/cita/delete_cita.html'
    success_url = reverse_lazy('admi:lista_cita')
    url_redirect = success_url
    permission_required = 'delete_cita'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EliminarCita, self).get_context_data(**kwargs)
        context['title'] = 'Eliminación de Cita'
        context['entity'] = 'Citas'
        context['list_url'] = reverse_lazy('admi:lista_cita')
        context['action'] = 'delete'
        return context


# Examenes

class listExamen(LoginRequiredMixin, PermisosGrupos, ListView):
    model = Examen
    template_name = 'admi/examen/list_examenes.html'
    permission_required = 'view_examen'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Examen.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Examenes'
        context['create_url'] = reverse_lazy('admi:crear_exa')
        context['list_url'] = reverse_lazy('admi:lista_exa')
        context['entity'] = 'Examen'
        return context


class crearExamen(LoginRequiredMixin, PermisosGrupos, CreateView):
    model = Examen
    template_name = 'admi/examen/crear_examen.html'
    form_class = ExamenForm
    success_url = reverse_lazy('admi:lista_exa')
    permission_required = 'add_examen'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Un Examen '
        context['entity'] = 'Examen'
        context['list_url'] = reverse_lazy('admi:lista_exa')
        context['action'] = 'add'
        return context


class editarExamen(LoginRequiredMixin, PermisosGrupos, UpdateView):
    model = Examen
    template_name = 'admi/examen/crear_examen.html'
    form_class = ExamenForm
    success_url = reverse_lazy('admi:lista_exa')
    permission_required = 'change_examen'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Un Examen '
        context['entity'] = 'Examen'
        context['list_url'] = reverse_lazy('admi:lista_exa')
        context['action'] = 'edit'
        return context


class eliminarExamen(LoginRequiredMixin, PermisosGrupos, DeleteView):
    model = Examen
    template_name = 'admi/examen/delete_examen.html'
    success_url = reverse_lazy('admi:lista_exa')
    permission_required = 'delete_examen'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un Examen'
        context['entity'] = 'Examen'
        context['list_url'] = reverse_lazy('admi:lista_exa')
        context['action'] = 'delete'
        return context


# Medicamento

class listMedicamento(LoginRequiredMixin, PermisosGrupos, ListView):
    model = Medicamento
    template_name = 'admi/medicamento/list_medicamento.html'
    permission_required = 'view_medicamento'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Medicamento.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Medicamentos'
        context['create_url'] = reverse_lazy('admi:crear_medica')
        context['list_url'] = reverse_lazy('admi:lista_medica')
        context['entity'] = 'Medicamento'
        return context


class crearMedicamento(LoginRequiredMixin, PermisosGrupos, CreateView):
    model = Medicamento
    template_name = 'admi/medicamento/crear_medicamento.html'
    form_class = MedicamentoForm
    success_url = reverse_lazy('admi:lista_medica')
    permission_required = 'add_medicamento'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Un Medicamento '
        context['entity'] = 'Medicamento'
        context['list_url'] = reverse_lazy('admi:lista_medica')
        context['action'] = 'add'
        return context


class editarMedicamento(LoginRequiredMixin, PermisosGrupos, UpdateView):
    model = Medicamento
    template_name = 'admi/medicamento/crear_medicamento.html'
    form_class = MedicamentoForm
    success_url = reverse_lazy('admi:lista_medica')
    permission_required = 'change_medicamento'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Un Medicamento '
        context['entity'] = 'Medicamento'
        context['list_url'] = reverse_lazy('admi:lista_medica')
        context['action'] = 'edit'
        return context


class eliminarMedicamento(LoginRequiredMixin, PermisosGrupos, DeleteView):
    model = Medicamento
    template_name = 'admi/medicamento/delete_medi.html'
    success_url = reverse_lazy('admi:lista_medica')
    permission_required = 'delete_medicamento'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un Medicamento'
        context['entity'] = 'Examen'
        context['list_url'] = reverse_lazy('admi:lista_medica')
        context['action'] = 'delete'
        return context


# Receta

class listReceta(LoginRequiredMixin, PermisosGrupos, ListView):
    model = Receta
    template_name = 'admi/receta/list_receta.html'
    permission_required = 'view_receta'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Receta.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Recetas'
        context['create_url'] = reverse_lazy('admi:crear_receta')
        context['list_url'] = reverse_lazy('admi:lista_receta')
        context['entity'] = 'Receta'
        return context


class crearReceta(LoginRequiredMixin, PermisosGrupos, CreateView):
    model = Receta
    template_name = 'admi/receta/crear_receta.html'
    form_class = RecetaForm
    success_url = reverse_lazy('admi:lista_receta')
    permission_required = 'add_receta'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear una receta  '
        context['entity'] = 'Receta'
        context['list_url'] = reverse_lazy('admi:lista_receta')
        context['action'] = 'add'
        return context


class editarReceta(LoginRequiredMixin, PermisosGrupos, UpdateView):
    model = Receta
    template_name = 'admi/receta/crear_receta.html'
    form_class = RecetaForm
    success_url = reverse_lazy('admi:lista_receta')
    permission_required = 'change_receta'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear una receta  '
        context['entity'] = 'Receta'
        context['list_url'] = reverse_lazy('admi:lista_receta')
        context['action'] = 'edit'
        return context


class eliminarReceta(LoginRequiredMixin, PermisosGrupos, DeleteView):
    model = Receta
    template_name = 'admi/receta/delete_receta.html'
    success_url = reverse_lazy('admi:lista_receta')
    permission_required = 'delete_receta'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de una Receta'
        context['entity'] = 'Receta'
        context['list_url'] = reverse_lazy('admi:lista_medica')
        context['action'] = 'delete'
        return context


# INTENTO REPORTES
class ReporteCita(LoginRequiredMixin, PermisosGrupos, ListView):
    model = Cita
    template_name = 'reportes/intentoreport.html'
    form_class = ReportForm
    permission_required = 'view_cita'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_report':
                data = []
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                search = Cita.objects.all()
                if len(start_date) and len(end_date):
                    search = search.filter(esp_medic__fecha_cita__range=[start_date, end_date])
                for i in search:
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Citas'
        context['create_url'] = reverse_lazy('admi:crear_cita')
        context['list_url'] = reverse_lazy('admi:lista_cita')
        context['entity'] = 'Listas'
        context['form'] = ReportForm()
        return context


class LogoutView(auth_views.LogoutView):
    next_page = '/'
