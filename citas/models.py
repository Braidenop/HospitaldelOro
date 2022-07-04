from datetime import datetime
from crum import get_current_request
from django.contrib.auth.models import AbstractUser
from django.forms import model_to_dict
from Intentocitas.settings import STATIC_URL, MEDIA_URL
from django.db import models


# Se utiliza una clase abstracta de donde se herederá los principales campos
# Campos de AbstractUser: id, username, email, first_name, last_name, password, 'user_permissions', 'last_login'
class Usuario(AbstractUser):
    image = models.ImageField(upload_to='users/%Y/%m/%d', null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Se especifica el campo a utilizar como Nombre de Usuario
    USERNAME_FIELD = 'username'
    # Se especifican los campos requeridos.
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    # Método para redireccionar la imagen a la carpeta media
    def get_image(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    # Método para serializar campos a tipo JSON
    def toJSON(self):
        item = model_to_dict(self,
                             exclude=['password', 'user_permissions', 'last_login'])
        if self.last_login:
            item['last_login'] = self.last_login.strftime('%Y-%m-%d')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['image'] = self.get_image()
        item['full_name'] = self.get_full_name()
        item['groups'] = [{'id': g.id, 'name': g.name} for g in self.groups.all()]
        return item

    # Método para mostrar la sesión actual
    def get_group_session(self):
        try:
            request = get_current_request()
            groups = self.groups.all()
            if groups.exists():
                if 'group' not in request.session:
                    request.session['group'] = groups[0]
        except:
            pass

    # Método que devuelve el nombre del objeto cuando se lo requiere
    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


class Especialidad(models.Model):
    nombre_esp = models.CharField(unique=True, blank=False, max_length=50)
    descrip = models.TextField(verbose_name='Descripción de Especialidad')

    def __str__(self):
        return self.nombre_esp

    # Método que configura datos con los que se interpretará el modelo
    class Meta:
        verbose_name = 'Especialidad'
        verbose_name_plural = 'Especialidades'

    def toJSON(self):
        item = model_to_dict(self)
        item['nombre_esp'] = self.nombre_esp
        item['descrip'] = self.descrip
        return item


class Medico(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    fecha_nacimiento = models.DateField(blank=False)
    edad = models.IntegerField(blank=True, verbose_name='Edad')
    telefono = models.CharField(max_length=10, blank=False, unique=True, verbose_name='Celular')
    cedula = models.CharField(max_length=10, unique=True, blank=False, verbose_name='Identificación')
    direccion = models.TextField(max_length=100, verbose_name='Dirección', blank=False, null=False)
    ciudad_red = models.CharField(max_length=30, verbose_name='Ciudad de Residencia', blank=False)
    masc = "Masculino"
    fem = "Femenino"
    choices_genero = (
        (masc, 'Masculino'), (fem, 'Femenino')
    )
    genero = models.CharField(blank=False, max_length=50, choices=choices_genero)

    # Método para calcular la Edad
    def age(self):
        return datetime.now().year - self.fecha_nacimiento.year

    # Método para guardar la edad
    def save(self, *args, **kwargs):
        self.edad = self.age()
        super(Medico, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Medico'
        verbose_name_plural = 'Medico'

    def __str__(self):
        return self.usuario.get_full_name()

    def toJSON(self):
        item = model_to_dict(self)
        item['usuario'] = self.usuario.toJSON()
        item['fecha_nacimiento'] = self.fecha_nacimiento
        item['edad'] = self.edad
        item['telefono'] = self.telefono
        item['cedula'] = self.cedula
        item['direccion'] = self.direccion
        item['ciudad_resid'] = self.ciudad_red
        item['genero'] = {'id': self.genero, 'name': self.get_genero_display()}

        return item


class Especialidad_Medico(models.Model):
    id_medico = models.ForeignKey(Medico, on_delete=models.CASCADE, verbose_name='Nombre del Medico')
    id_especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE,
                                        verbose_name='Nombre de la Especialidad')

    Lunes = 'Lunes'
    Martes = 'Martes'
    Miercoles = 'Miercoles'
    Jueves = 'Jueves'
    Viernes = 'Viernes'

    Dias_Laborables = [
        (Lunes, 'Lunes'),
        (Martes, 'Martes'),
        (Miercoles, 'Miercoles'),
        (Jueves, 'Jueves'),
        (Viernes, 'Viernes'),
    ]

    dia_laboral = models.CharField(max_length=20, choices=Dias_Laborables, help_text='Seleccione un dia',
                                   verbose_name='Dia Laboral')

    horario_1 = '8:h00 - 8h30'
    horario_2 = '8h30 - 9h00'
    horario_3 = '9h00 - 10h00'
    horario_4 = '10h00 - 10h30'
    horario_5 = '10h30 - 11h00'
    horario_6 = '11h30 - 12h00'
    horario_7 = '12:h00 - 12h30'
    horario_8 = '12h30 - 13h00'
    horario_9 = '13h00 - 13h30'
    horario_10 = '13h30 - 14h00'
    horario_11 = '14h300 - 14h00'
    horario_12 = '14h00 - 14h30'
    horario_13 = '14:h30 - 15h00'
    horario_14 = '15h00 - 15h30'
    horario_15 = '15h30 - 16h00'
    horario_16 = '16h00 - 16h30'
    horario_17 = '16h30 - 17h00'
    horario_18 = '17h00 - 17h30'
    horario_19 = '17h30 - 18h00'

    Horarios_de_Atencion = [
        (horario_1, '8:h00 - 8h30'),
        (horario_2, '8h30 - 9h00'),
        (horario_3, '9h00 - 10h00'),
        (horario_4, '10h00 - 10h30'),
        (horario_5, '10h30 - 11h00'),
        (horario_6, '11h30 - 12h00'),
        (horario_7, '12:h00 - 12h30'),
        (horario_8, '12h30 - 13h00'),
        (horario_9, '13h00 - 13h30'),
        (horario_10, '13h30 - 14h00'),
        (horario_11, '14h300 - 14h00'),
        (horario_12, '14h00 - 14h30'),
        (horario_13, '14:h30 - 15h00'),
        (horario_14, '15h00 - 15h30'),
        (horario_15, '15h30 - 16h00'),
        (horario_16, '16h00 - 16h30'),
        (horario_17, '16h30 - 17h00'),
        (horario_18, '17h00 - 17h30'),
        (horario_19, '17h30 - 18h00'),
    ]

    horario = models.CharField(max_length=30, choices=Horarios_de_Atencion, help_text='Seleccione el horario',
                               verbose_name='Horario de Atención')

    consul1 = 'Consultorio 1'
    consul2 = 'Consultorio 2'
    consul3 = 'Consultorio 3'
    consul4 = 'Consultorio 4'

    consultorios = [
        (consul1, 'Consultorio 1'),
        (consul2, 'Consultorio 2'),
        (consul3, 'Consultorio 3'),
        (consul4, 'Consultorio 4'),
    ]

    consul = models.CharField(max_length=20, choices=consultorios, help_text='Seleccione un consultorio',
                              verbose_name='Consultorio')

    def __str__(self):
        return "%s %s %s %s %s " % (self.id_medico, self.id_especialidad, self.dia_laboral, self.horario, self.consul)

    # Metodo para establecer restricciones del módelo e impedir que dos Medicos tengan datos repetidos.
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["id_medico", "id_especialidad", "dia_laboral", "horario"], name="med_esp_di_hh"
            ),
            models.UniqueConstraint(
                fields=["dia_laboral", "horario", "consul"], name="med_esp"
            ),

        ]

    def toJSON(self):
        item = model_to_dict(self)
        item['id_medico'] = self.id_medico.toJSON()
        item['id_especialidad'] = self.id_especialidad.toJSON()
        item['dia_laboral'] = {'id': self.dia_laboral, 'name': self.get_dia_laboral_display()}
        item['horario'] = {'id': self.horario, 'name': self.get_horario_display()}
        item['consul'] = {'id': self.consul, 'name': self.get_consul_display()}
        return item


class Paciente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='usuarioP')
    fecha_nacimiento = models.DateField(blank=False)
    edad = models.IntegerField(blank=True, verbose_name='Edad')
    telefono = models.CharField(max_length=10, blank=False, unique=True, verbose_name='Celular')
    cedula = models.CharField(max_length=10, unique=True, blank=False, verbose_name='Identificación')
    direccion = models.TextField(max_length=100, verbose_name='Dirección', blank=False, null=False)
    ciudad_red = models.CharField(max_length=30, verbose_name='Ciudad de Residencia', blank=False)
    masc = "Masculino"
    fem = "Femenino"
    choices_genero = (
        (masc, 'Masculino'), (fem, 'Femenino')
    )
    genero = models.CharField(blank=False, max_length=50, choices=choices_genero)

    def age(self):
        return datetime.now().year - self.fecha_nacimiento.year

    def save(self, *args, **kwargs):
        self.edad = self.age()
        super(Paciente, self).save(*args, **kwargs)

    def toJSON(self):
        item = model_to_dict(self)
        item['usuario'] = self.usuario.toJSON()
        item['fecha_nacimiento'] = self.fecha_nacimiento
        item['edad'] = self.edad
        item['telefono'] = self.telefono
        item['cedula'] = self.cedula
        item['direccion'] = self.direccion
        item['ciudad_resid'] = self.ciudad_red
        item['genero'] = {'id': self.genero, 'name': self.get_genero_display()}

        return item

    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'

    def __str__(self):
        return self.usuario.get_full_name(), self.telefono


class Cita(models.Model):
    paciente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    esp_medic = models.ForeignKey(Especialidad_Medico, on_delete=models.CASCADE, verbose_name='Disponibilidad')
    fecha_cita = models.DateField(default=datetime.now)

    Consulta = 'Consulta'
    RevisionExamenes = 'Revisión de Exámenes'
    Otro = 'Otro'

    motivo_choices = [
        (Consulta, 'Consulta'),
        (RevisionExamenes, 'Revisión de Exámenes'),
        (Otro, 'Otro'),
    ]

    motivo = models.CharField(max_length=20, verbose_name='Motivo de cita', choices=motivo_choices)

    def __str__(self):
        return "%s %s %s %s" % (self.paciente, self.esp_medic, self.fecha_cita, self.motivo)

    def toJSON(self):
        item = model_to_dict(self)
        item['paciente'] = self.paciente.toJSON()
        item['esp_medic'] = self.esp_medic.toJSON()
        item['fecha_cita'] = self.fecha_cita.strftime('%Y-%m-%d')
        item['motivo'] = {'id': self.motivo, 'name': self.get_motivo_display()}

        return item

    class Meta:
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'
        unique_together = ['esp_medic', 'fecha_cita']


class Medicamento(models.Model):
    nombre = models.CharField(blank=False, max_length=50)
    presentacion = models.CharField(blank=False, max_length=50)
    volumen = models.CharField(blank=False, max_length=50)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return '%s %s' % (self.nombre, self.presentacion)

    class Meta:
        verbose_name = 'Medicamento'
        verbose_name_plural = 'Medicamentos'

    def toJSON(self):
        item = model_to_dict(self)
        item['nombre'] = self.nombre
        item['presentacion'] = self.presentacion
        item['volumen'] = self.volumen
        item['descrip'] = self.descripcion
        return item


class Consulta(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)

    diagnostico = models.TextField(blank=False)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.paciente, self.medico)

    class Meta:
        verbose_name = 'Consulta'
        verbose_name_plural = 'Consultas'


class Receta(models.Model):
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE, verbose_name='Medicamento')
    descripcion = models.CharField(max_length=200, blank=False, verbose_name='Indicación')

    class Meta:
        verbose_name = 'Tratamiento'
        verbose_name_plural = 'Tratamientos'

    def __str__(self):
        return '%s %s' % (self.medicamento, self.descripcion)

    def toJSON(self):
        item = model_to_dict(self)
        item['medicamento'] = self.medicamento.toJSON()
        item['descripcion'] = self.descripcion
        return item


class Consultorio(models.Model):
    nombre = models.CharField(blank=False, max_length=50)
    direccion = models.TextField(blank=False)
    mision = models.TextField(blank=False)
    vision = models.TextField(blank=False)
    eslogan = models.CharField(blank=False, max_length=150)
    telefono = models.CharField(blank=False, max_length=50)
    correo = models.EmailField(blank=False)
    foto = models.ImageField(upload_to='home')


class Examen(models.Model):
    nombre = models.CharField(max_length=100, unique=True, blank=False, verbose_name='Nombre del Examen')
    descrip = models.CharField(max_length=100, verbose_name='Descripción del Examen')

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        item['nombre'] = self.nombre
        item['descrip'] = self.descrip
        return item


class Historiaclinica(models.Model):
    id_cita = models.ForeignKey(Cita, on_delete=models.CASCADE, verbose_name='Cita')
    diagnostico = models.TextField(verbose_name='Diagnóstico')
    examen = models.ManyToManyField(Examen)
    receta = models.ManyToManyField(Receta)

    def __str__(self):
        return '%s %s %s' % (self.id_cita, self.examen, self.receta)

    # Muestra una lista de los examenes a seleccionar
    def display_examen(self):
        return ', '.join([examen.nombre for examen in self.examen.all()])

    display_examen.short_description = 'Examen'

    # Muestra una lista de las recetas a seleccionar
    def display_rece(self):
        return ', '.join([receta.medicamento.descripcion for receta in self.receta.all()])

    display_rece.short_description = 'Receta'
