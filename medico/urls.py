from django.urls import path
from medico.views import *

app_name = 'medico'

urlpatterns = [
    path('', homeMedico.as_view(), name='home_medico'),
    path('perfil', perfilMedico.as_view(), name='perfil_medico'),
    path('citas', ListaCita.as_view(), name='citas'),
    path('registro', RegistroMedico.as_view(), name='registro_medico'),
    # path('login', LoginMedico.as_view(), name='login_medico'),
    path('logout', LogoutView.as_view(), name='logout_medico'),
    #Consultas
    path('historia/pdf/<int:pk>/', RecetaPDF.as_view(), name='receta_pdf'),
    path('lista_Consultas/', ConsultaList.as_view(), name='lista_consul'),
    # path('crearHis/', HistoriaCrear.as_view(), name='crear_hist'),
    path('crearConsul/', consul_crear, name='crear_consul'),
    path('editar_Consul/<int:pk>/', EditarConsul.as_view(), name='editar_consul'),
    path('eliminar_Consul/<int:pk>/', EliminarConsul.as_view(), name='eliminar_consul'),


]