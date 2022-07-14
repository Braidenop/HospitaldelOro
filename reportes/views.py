from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from citas.models import Cita

from reportes.forms import ReportForm


class Reportes(TemplateView):
    template_name = 'reportes/report.html'

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
                    search = search.filter(esp_medic__fecha_cita__range=[start_date, end_date])
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
        context['title'] = 'Reporte de Citas'
        context['entity'] = 'Reportes'
        context['list_url'] = reverse_lazy('reportes:report_cita')
        context['form'] = ReportForm()
        return context
