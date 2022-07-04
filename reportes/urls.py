from django.urls import path
from reportes.views import Reportes

app_name = 'reportes'

urlpatterns = [
    path('cita/', Reportes.as_view(), name='report_cita'),
]
