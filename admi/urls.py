from django.urls import path
from admi.views import *

app_name = 'admi'

urlpatterns = [
    # Usuario
    path('', homeAdmin.as_view(), name='home'),
    path('list_usuarios/', listUsuarios.as_view(), name='lista_usuarios'),
    path('creación_usuario/', crearUsuario.as_view(), name='crear_usuario'),
    path('editar_usuario/<int:pk>/', editarUsuario.as_view(), name='editar_usuario'),
    path('eliminar_usuario/<int:pk>/', eliminarUsuario.as_view(), name='eliminar_usuario'),

    # Paciente
    path('list_pacie/', listPacientes.as_view(), name='lista_pacie'),
    path('creación_pacie/', crearPaciente.as_view(), name='crear_pacie'),
    path('editar_pacie/<int:pk>/', editarPaciente.as_view(), name='editar_pacie'),
    path('eliminar_pacie/<int:pk>/', eliminarPaciente.as_view(), name='eliminar_pacie'),

    # Especialidad
    path('list_espe/', listEspe.as_view(), name='lista_espe'),
    path('creación_espe/', crearEspe.as_view(), name='crear_espe'),
    path('editar_espe/<int:pk>/', editarEspe.as_view(), name='editar_espe'),
    path('eliminar_espe/<int:pk>/', eliminarEspe.as_view(), name='eliminar_espe'),

    # Medicos
    path('list_medi/', listMedi.as_view(), name='lista_medi'),
    path('creación_medi/', crearMedi.as_view(), name='crear_medi'),
    path('editar_medi/<int:pk>/', editarMedi.as_view(), name='editar_medi'),
    path('eliminar_medi/<int:pk>/', eliminarMedi.as_view(), name='eliminar_medi'),

    # Disponibilidad
    path('list_dipo/', listDispo.as_view(), name='lista_dipo'),
    path('creación_dipo/', crearDispo.as_view(), name='crear_dipo'),
    path('editar_dipo/<int:pk>/', editarDispo.as_view(), name='editar_dipo'),
    path('eliminar_dipo/<int:pk>/', eliminarDispo.as_view(), name='eliminar_dipo'),

    # Cita
    path('list_cita/', AgendaCita.as_view(), name='lista_cita'),
    path('creación_cita/', CrearCita.as_view(), name='crear_cita'),
    path('editar_cita/<int:pk>/', EditarCita.as_view(), name='editar_cita'),
    path('eliminar_cita/<int:pk>/', EliminarCita.as_view(), name='eliminar_cita'),
    path('intlist_cita/', ReporteCita.as_view(), name='intlista_cita'),
    #Examenes
    path('list_examen/', listExamen.as_view(), name='lista_exa'),
    path('creacion_examen/', crearExamen.as_view(), name='crear_exa'),
    path('editar_examen/<int:pk>/', editarExamen.as_view(), name='editar_exa'),
    path('eliminar_examen/<int:pk>/', eliminarExamen.as_view(), name='eliminar_exa'),

    #Medicamento
    path('list_medicament/', listMedicamento.as_view(), name='lista_medica'),
    path('creacion_medicament/', crearMedicamento.as_view(), name='crear_medica'),
    path('editar_medicament/<int:pk>/', editarMedicamento.as_view(), name='editar_medica'),
    path('eliminar_medicament/<int:pk>/', eliminarMedicamento.as_view(), name='eliminar_medica'),

    #Receta
    path('list_receta/', listReceta.as_view(), name='lista_receta'),
    path('creacion_receta/', crearReceta.as_view(), name='crear_receta'),
    path('editar_receta/<int:pk>/', editarReceta.as_view(), name='editar_receta'),
    path('eliminar_receta/<int:pk>/', eliminarReceta.as_view(), name='eliminar_receta'),

    path('logout', LogoutView.as_view(), name='logout'),
]
