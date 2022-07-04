from django.contrib import admin
from .models import Especialidad, Medico, Paciente, Especialidad_Medico, Cita, Usuario, Medicamento, Receta, \
    Historiaclinica, Examen


class MedicamentoAdmin(admin.ModelAdmin):
    model = Medicamento
    list_display = ('nombre', 'presentacion', 'volumen', 'descripcion')


class ExamenesAdmin(admin.ModelAdmin):
    model = Examen
    list_display = ('nombre', 'descrip')


class Tratamientodmin(admin.ModelAdmin):
    model = Receta
    list_display = ('medicamento', 'descripcion',)


class HistoriaCliAdmin(admin.ModelAdmin):
    model = Historiaclinica
    list_display = ('id_cita', 'diagnostico', 'display_examen', 'display_rece')


class EspecialidadAdmin(admin.ModelAdmin):
    model = Especialidad
    list_display = ('nombre_esp', 'descrip')


class MedicoAdmin(admin.ModelAdmin):
    model = Medico
    list_display = ('usuario', 'cedula', 'direccion',
                    'telefono', 'genero')
    search_fields = ('cedula', 'usuario')


class PacienteAdmin(admin.ModelAdmin):
    model = Paciente
    list_display = ('usuario', 'cedula', 'direccion',
                    'telefono', 'genero',)


class Espcialidad_MedicoAdmin(admin.ModelAdmin):
    model = Especialidad_Medico
    list_display = ('id_medico', 'id_especialidad', 'dia_laboral', 'horario')


class CitAdmin(admin.ModelAdmin):
    model = Cita


admin.site.register(Usuario)
admin.site.register(Medico, MedicoAdmin)
admin.site.register(Especialidad, EspecialidadAdmin)
admin.site.register(Paciente, PacienteAdmin)
admin.site.register(Cita, CitAdmin)
admin.site.register(Especialidad_Medico, Espcialidad_MedicoAdmin)
admin.site.register(Medicamento, MedicamentoAdmin)
admin.site.register(Examen, ExamenesAdmin)
admin.site.register(Receta, Tratamientodmin)
admin.site.register(Historiaclinica, HistoriaCliAdmin)
