from django.forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.forms import DateInput

from .models import Usuario, Paciente, Cita


class LoginForm(Form):
    username = CharField(max_length=30,
                               widget=TextInput(attrs={'required': 'True'}))
    password = CharField(max_length=30,
                               widget=TextInput(attrs={'type': 'password', 'required': 'True'}))


class RegistroUsuarioForm(ModelForm):
    passwordCheck = CharField(max_length=30, widget=TextInput(
        attrs={'class': '',

               'required': 'True',
               'type': 'password'
               }))

    class Meta:
        model = Usuario
        fields = ('first_name', 'last_name', 'email', 'username', 'password', 'image')
        widgets = {
            'username': TextInput(attrs=
            {
                'class': '',
            }),
            'email': TextInput(attrs=
            {
                'type': 'email',
                'class': '',
            }),
            'password': TextInput(attrs=
            {
                'type': 'password',
                'class': '',
                'required': 'True'
            }),
            'first_name': TextInput(
                attrs=
                {
                    'class': '',
                    'required': 'True'
                }
            ),
            'last_name': TextInput(
                attrs=
                {
                    'class': '',
                    'required': 'True'
                }
            ),
        }

        exclude = ['user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_active', 'is_staff']

    def clean_password(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.data.get('passwordCheck')

        if not password2:
            raise forms.ValidationError("Debes verificar tu contraseña.")
        if password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2


class DateImput(DateInput):
    input_type = 'date'


class RegistroPacienteForm(ModelForm):
    class Meta:
        model = Paciente
        exclude = ('usuario', 'edad')
        widgets = {
            'fecha_nacimiento': DateImput(attrs={'class': 'form-control'}),
            'cedula': TextInput(),
            'direccion': TextInput(attrs={'class': 'materialize-textarea'}),
            'genero': Select(attrs={'class': 'browser-default'}),
            'telefono': TextInput(),
            'ciudad_red': TextInput(),

        }


class AgendaCitaForm(ModelForm):
    # def __init__(self, *args, **kwargs):
    #     user = kwargs.pop('user')
    #     self.paciente = user
    #     super(AgendaCitaForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Cita
        fields = ['esp_medic', 'fecha_cita', 'motivo']
        widgets = {
            'esp_medic': Select(attrs={
                'class ': 'form-control select2',
            }
            ),
            'fecha_cita': DateInput(),
            'motivo': Select(),

        }

    # def save(self, *args, **kwargs):
    #     self.instance.paciente = self.paciente
    #     cita = super(AgendaCitaForm, self).save(*args,**kwargs)
    #     return cita


class FormularioLogin(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(FormularioLogin, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Nombre de Usuario'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Contraseña'
