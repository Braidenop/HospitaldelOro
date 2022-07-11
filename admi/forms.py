from django import forms
from django.forms import DateTimeInput, DateInput, SelectMultiple, PasswordInput, TextInput, ModelForm, EmailInput
from citas.models import Usuario, Especialidad, Medico, Especialidad_Medico, Cita, Examen, Medicamento, Receta, \
    Paciente, Consulta
from django.contrib.auth.forms import UserCreationForm


# Formulario para creación de usuario dentro del Administrador
class CrearUsuarioForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = Usuario
        fields = 'username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'image', 'groups'
        widgets = {
            'username': TextInput(
                attrs={
                    'placeholder': 'Ingrese su username',
                }
            ),
            'password1': PasswordInput(
                attrs={
                    'placeholder': 'Ingrese su password',
                }
            ),
            'password2': PasswordInput(
                attrs={
                    'placeholder': 'Ingrese su password',
                }
            ),
            'first_name': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus nombres',
                }
            ),
            'last_name': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus apellidos',
                }
            ),
            'groups': SelectMultiple(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'multiple': 'multiple'
            })
        }

    def save(self, commit=True):
        form = super()
        if form.is_valid():
            u = form.save(commit=False)
            u.save()
            for g in self.cleaned_data['groups']:
                u.groups.add(g)
        return form


# Formulario para editar usuario
class EditarUsuarioForm(ModelForm):
    class Meta:
        model = Usuario
        fields = 'username', 'password', 'groups', 'email', 'first_name', 'last_name', 'image'
        widgets = {
            'username': TextInput(
                attrs={
                    'placeholder': 'Ingrese su username',
                }
            ),
            'password': PasswordInput(render_value=True,
                                      attrs={
                                          'placeholder': 'Ingrese su password',
                                      }
                                      ),
            'first_name': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus nombres',
                }
            ),
            'last_name': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus apellidos',
                }
            ),
            'groups': SelectMultiple(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'multiple': 'multiple'
            }),

            'email': EmailInput(),
        }

    # Método para guardar la instancia del formulario con los detalles de grupos y clave diferente
    def save(self, commit=True):
        form = super()
        if form.is_valid():
            pwd = self.cleaned_data['password']
            u = form.save(commit=False)
            if u.pk is None:
                u.set_password(pwd)
            else:
                user = Usuario.objects.get(pk=u.pk)
                if user.password != pwd:
                    u.set_password(pwd)
            u.save()
            u.groups.clear()
            for g in self.cleaned_data['groups']:
                u.groups.add(g)
        return form


# Formulario para especialidad
class EspecialidadForm(forms.ModelForm):
    # Método que permite enviar un parametro inicial en el form
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre_esp'].widget.attrs['autofocus'] = True

    class Meta:
        model = Especialidad
        fields = '__all__'
        widgets = {
            'nombre_esp': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese una Especialidad ',
                }
            ),
            'descrip': forms.Textarea(
                attrs={
                    'placeholder': 'Ingrese la Descripción',

                }
            ),
        }


# Clase para cambiar el tipo de dato de entrada en el input
class DateImput(DateInput):
    input_type = 'date'


# Formulario para crear Médico
class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        exclude = ('edad', 'fecha_nacimiento')
        widgets = {
            'usuario': forms.Select(attrs={'class': 'browser-default'}),
            # 'fecha_nacimiento': DateImput(),
            'cedula': forms.TextInput(),
            'direccion': forms.TextInput(attrs={'class': 'materialize-textarea'}),
            'genero': forms.Select(attrs={'class': 'browser-default'}),
            'telefono': forms.TextInput(),
            'ciudad_red': forms.TextInput(),
            'esp': forms.SelectMultiple(),
        }


# Formulario para crear Paciente
class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        exclude = ('edad',)
        widgets = {
            'usuario': forms.Select(attrs={'class': 'browser-default'}),
            'cedula': forms.TextInput(),
            'direccion': forms.TextInput(attrs={'class': 'materialize-textarea'}),
            'genero': forms.Select(attrs={'class': 'browser-default'}),
            'telefono': forms.TextInput(),
            'ciudad_red': forms.TextInput(),

        }


# Formulario para crear Disponibilidad
class DisponibilidadForm(forms.ModelForm):
    class Meta:
        model = Especialidad_Medico
        fields = ['id_medico', 'id_especialidad', 'fecha_cita', 'horario', 'consul']
        widgets = {
            'id_medico': forms.Select(attrs={'class': 'browser-default'}),
            'id_especialidad': forms.Select(attrs={'class': 'browser-default'}),
            'horario': forms.Select(attrs={'class': 'browser-default'}),
            'consul': forms.Select(attrs={'class': 'browser-default'}),
            'fecha_cita': DateImput(attrs={'class': 'form-control'}),
        }


# Formulario para crear Cita
class CitaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CitaForm, self).__init__(*args, **kwargs)
        self.fields['paciente'].queryset = Usuario.objects.filter(groups__name='Paciente')
        self.fields['esp_medic'].queryset = Especialidad_Medico.objects.filter(dispo=False)

    class Meta:
        model = Cita
        fields = ['paciente', 'esp_medic', 'motivo']
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-control select2'}),
            'esp_medic': forms.Select(attrs={'class': 'browser-default'}),
            'motivo': forms.Select(attrs={'class': 'browser-default'}),
        }


# Formulario para crear Examen
class ExamenForm(forms.ModelForm):
    class Meta:
        model = Examen
        fields = ['nombre', 'descrip']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'descrip': forms.Textarea(attrs={'placeholder': 'Ingrese una Descripción'}),
        }


# Formulario para crear Medicamento
class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = ['nombre', 'presentacion', 'volumen', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'presentacion': forms.TextInput(attrs={'placeholder': 'Ingrese una Presentación'}),
            'volumen': forms.TextInput(attrs={'placeholder': 'Ingrese un Volumen'}),
            'descripcion': forms.Textarea(attrs={'placeholder': 'Ingrese una Descripción'}),
        }


# Formulario para crear Receta
class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = ['medicamento', 'descripcion']
        widgets = {
            'medicamento': forms.Select(attrs={'class': 'browser-default'}),
            'descripcion': forms.TextInput(attrs={'placeholder': 'Ingrese la indicación'}),
        }
