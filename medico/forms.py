from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import DateInput
from citas.models import Usuario, Medico, Cita, Consulta


class RegistroUsuarioForm(forms.ModelForm):
    passwordCheck = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={'class': '',

               'required': 'True',
               'type': 'password'
               }))

    class Meta:
        fields = ('first_name', 'last_name', 'email', 'username', 'password', 'image')
        widgets = {
            'username': forms.TextInput(attrs=
            {
                'class': '',
            }),
            'email': forms.TextInput(attrs=
            {
                'type': 'email',
                'class': '',
            }),
            'password': forms.TextInput(attrs=
            {
                'type': 'password',
                'class': '',
                'required': 'True'
            }),
            'first_name': forms.TextInput(

            ),
            'last_name': forms.TextInput(

            ),
        }

        exclude = ['user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_active', 'is_staff']

    def clean_password(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.data.get('passwordCheck')
        print(password2)

        if not password2:
            raise forms.ValidationError("Debes verificar tu contraseña.")
        if password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2


class DateImput(DateInput):
    input_type = 'date'


class RegistroMedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        exclude = ('usuario', 'edad')
        widgets = {
            'fecha_nacimiento': DateImput(),
            'cedula': forms.TextInput(),
            'direccion': forms.TextInput(attrs={'class': 'materialize-textarea'}),
            'genero': forms.Select(attrs={'class': 'browser-default'}),
            'telefono': forms.TextInput(),
            'ciudad_red': forms.TextInput(),
        }


class FormularioLogin(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(FormularioLogin, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Nombre de Usuario'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Contraseña'


class ConsultaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(ConsultaForm, self).__init__(*args, **kwargs)
        self.fields['id_cita'].queryset = Cita.objects.select_related().filter(
            esp_medic__id_medico__usuario=self.request.user, estado=False)

    class Meta:
        model = Consulta
        fields = ['id_cita', 'diagnostico', 'examen', 'receta', 'tipo_enf']
        widgets = {
            'diagnostico': forms.Textarea(attrs={'placeholder': 'Ingrese el Diagnóstico', }),
            'examen': forms.SelectMultiple(attrs={'class': 'form-control select2',
                                                  'style': 'width: 100%',
                                                  'multiple': 'multiple'}),
            'receta': forms.SelectMultiple(attrs={'class': 'form-control select2',
                                                  'style': 'width: 100%',
                                                  'multiple': 'multiple'}),
            'tipo_enf': forms.Select(),
        }
