from django.urls import path
from medico.views import *

app_name = 'medico'

urlpatterns = [
    path('', homeMedico.as_view(), name='home_medico'),
    path('citas', ListaCita.as_view(), name='citas'),
    path('registro', RegistroMedico.as_view(), name='registro_medico'),
    # path('login', LoginMedico.as_view(), name='login_medico'),
    path('logout', LogoutView.as_view(), name='logout_medico'),
    #Historia Clínica
    path('historia/pdf/<int:pk>/', RecetaPDF.as_view(), name='receta_pdf'),
    path('lista_historiacli/', HistoriaList.as_view(), name='lista_hist'),
    # path('crearHis/', HistoriaCrear.as_view(), name='crear_hist'),
    path('crearHis/', hist_crear, name='crear_hist'),
    path('editar_His/<int:pk>/', EditarHist.as_view(), name= 'editar_hist' ),
    path('eliminar_His/<int:pk>/', EliminarHist.as_view(), name='eliminar_hist'),


]