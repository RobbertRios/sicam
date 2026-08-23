import os
import hashlib
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from PIL import Image
from django.conf import settings

from django.contrib.postgres.indexes import GinIndex
from django.db.models import Q

# ============================================================================
# UTILIDADES DE ARCHIVOS
# ============================================================================

def generar_nombre_estructurado(instance, filename, subcarpeta, tipo_mascara=None):
    extension = os.path.splitext(filename)[1].lower()
    ahora = datetime.now()
    timestamp = ahora.strftime('%Y%m%d_%H%M%S')
    
    if hasattr(instance, 'id_caso_fk'):
        caso = instance.id_caso_fk
        tipo_ref = instance.tipo_muestra.upper()
        tipo_muestra_path = instance.tipo_muestra.lower()
    else:
        caso = instance.id_analisis_fk.id_muestra_fk.id_caso_fk
        tipo_muestra_path = instance.id_analisis_fk.id_muestra_fk.tipo_muestra.lower()
        if tipo_mascara:
            tipo_ref = tipo_mascara
        else:
            tipo_ref = instance.tipo.upper().replace('MASCARA_', '')

    paciente = caso.id_paciente_fk
    ini_n = paciente.nombre[0].upper() if paciente.nombre else 'X'
    ini_a = paciente.apellido[0].upper() if paciente.apellido else 'X'
    iniciales = f"{ini_n}{ini_a}"
    id_caso_str = f"C{str(caso.id_caso).zfill(4)}"
    hash_txt = hashlib.md5(filename.encode()).hexdigest()[:6]
    nombre_final = f"{iniciales}_{id_caso_str}_{tipo_ref}_{timestamp}_{hash_txt}{extension}"

    return os.path.join(
        subcarpeta, 
        tipo_muestra_path, 
        ahora.strftime('%Y'), 
        ahora.strftime('%m'), 
        nombre_final
    )


def path_muestras(instance, filename):
    return generar_nombre_estructurado(instance, filename, 'muestras')


def path_mascaras(instance, filename):
    tipo_mascara = None
    if hasattr(instance, 'tipo'):
        if 'nucleo' in instance.tipo.lower():
            if 'micro' in instance.tipo.lower():
                tipo_mascara = 'MICRONUCLEO'
            else:
                tipo_mascara = 'NUCLEO'
        elif 'membrana' in instance.tipo.lower():
            tipo_mascara = 'MEMBRANA'
    return generar_nombre_estructurado(instance, filename, 'mascaras', tipo_mascara)


def path_previews(instance, filename):
    return generar_nombre_estructurado(instance, filename, 'previews')


def path_json_raw(instance, filename):
    return generar_nombre_estructurado(instance, filename, 'json_raw')


# ============================================================================
# DOCTOR — perfil médico ligado al User de Django
# ============================================================================

class Doctor(models.Model):
    """
    Perfil de doctor. Extiende django.contrib.auth.User (OneToOne).
    El User maneja email, password y is_active.
    Este modelo agrega los datos clínicos del médico.
    """
    ESPECIALIDAD_CHOICES = [
        ('genetica', 'Genética Médica'),
        ('oncologia', 'Oncología'),
        ('hematologia', 'Hematología'),
        ('patologia', 'Patología'),
        ('medicina_interna', 'Medicina Interna'),
        ('otro', 'Otro'),
    ]

    id_doctor       = models.AutoField(primary_key=True)
    user            = models.OneToOneField(
                          User,
                          on_delete=models.CASCADE,
                          related_name='doctor'
                      )
    nombre          = models.CharField(max_length=100)
    apellido        = models.CharField(max_length=100)
    cedula_prof     = models.CharField(max_length=50, unique=True, help_text="Cédula profesional")
    especialidad    = models.CharField(max_length=30, choices=ESPECIALIDAD_CHOICES, default='otro')
    institucion     = models.CharField(max_length=200, blank=True, null=True)
    telefono        = models.CharField(max_length=20, blank=True, null=True)
    fecha_registro  = models.DateTimeField(auto_now_add=True)
    activo          = models.BooleanField(default=True)

    class Meta:
        db_table = 'doctor'

    def __str__(self):
        return f"Dr. {self.nombre} {self.apellido} ({self.user.email})"

    @property
    def nombre_completo(self):
        return f"Dr. {self.nombre} {self.apellido}"


# ============================================================================
# PACIENTE
# ============================================================================

class Paciente(models.Model):
    id_paciente     = models.AutoField(primary_key=True)
    # FK al doctor que registró/atiende este paciente
    id_doctor_fk    = models.ForeignKey(
                          Doctor,
                          on_delete=models.SET_NULL,
                          null=True,
                          blank=True,
                          related_name='pacientes',
                          help_text="Doctor responsable del paciente"
                      )
    nombre          = models.CharField(max_length=100)
    apellido        = models.CharField(max_length=100)
    identificacion  = models.CharField(max_length=50, unique=True)
    fecha_nacimiento= models.DateField()
    email           = models.EmailField(blank=True, null=True)
    telefono        = models.CharField(max_length=20, blank=True, null=True)
    fecha_registro  = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'paciente'
    
    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.identificacion})"


class CasoClinico(models.Model):
    ESTADO_CHOICES = [
        ('abierto', 'Abierto'), 
        ('en_proceso', 'En Proceso'), 
        ('cerrado', 'Cerrado')
    ]
    
    id_caso         = models.AutoField(primary_key=True)
    id_paciente_fk  = models.ForeignKey(
                          Paciente, 
                          on_delete=models.CASCADE, 
                          related_name='casos'
                      )
    fecha_inicio    = models.DateTimeField(auto_now_add=True)
    estado          = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='abierto')
    diagnostico     = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'caso_clinico'
    
    def __str__(self):
        return f"Caso {self.id_caso} - {self.id_paciente_fk.nombre}"


class Muestra(models.Model):
    TIPO_CHOICES = [
        ('sangre', 'Sangre'),
        ('saliva', 'Saliva')
    ]

    id_muestra      = models.AutoField(primary_key=True)
    id_caso_fk      = models.ForeignKey(
                          CasoClinico,
                          on_delete=models.CASCADE,
                          related_name='muestras'
                      )
    tipo_muestra    = models.CharField(max_length=20, choices=TIPO_CHOICES, default='saliva')
    ruta_imagen     = models.ImageField(upload_to=path_muestras)
    thumbnail       = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    fecha_toma      = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'muestras'

    def __str__(self):
        return f"Muestra {self.id_muestra} ({self.tipo_muestra})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.ruta_imagen and not self.thumbnail:
            img_path = self.ruta_imagen.path
            img = Image.open(img_path)
            img.thumbnail((300, 300))
            base_name = os.path.basename(self.ruta_imagen.name)
            thumb_name = f"thumb_{base_name}"
            thumb_relative_path = os.path.join('thumbnails', thumb_name)
            thumb_full_path = os.path.join(settings.MEDIA_ROOT, thumb_relative_path)
            os.makedirs(os.path.dirname(thumb_full_path), exist_ok=True)
            img.save(thumb_full_path)
            self.thumbnail = thumb_relative_path
            super().save(update_fields=['thumbnail'])


class Analisis(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'), 
        ('proceso', 'En Proceso'), 
        ('listo', 'Listo'), 
        ('error', 'Error')
    ]
    
    id_analisis     = models.AutoField(primary_key=True)
    id_muestra_fk   = models.ForeignKey(
                          Muestra, 
                          on_delete=models.CASCADE, 
                          related_name='analisis'
                      )
    version_modelo  = models.CharField(max_length=50)
    estado          = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    fecha_ejecucion = models.DateTimeField(auto_now_add=True)

    requiere_revision_manual = models.BooleanField(default=False, help_text="Marca si el análisis necesita revisión humana")

    class Meta:
        db_table = 'analisis'
    
    def __str__(self):
        return f"Análisis {self.id_analisis} - {self.estado}"


class AnalisisResultados(models.Model):
    id_resultado        = models.AutoField(primary_key=True)
    id_analisis_fk      = models.OneToOneField(
                              Analisis,
                              on_delete=models.CASCADE,
                              related_name='resultados'
                          )
    total_membranas     = models.IntegerField(default=0)
    total_nucleos       = models.IntegerField(default=0)
    total_micronucleos  = models.IntegerField(default=0)
    total_binucleadas   = models.IntegerField(default=0)
    total_trinucleadas  = models.IntegerField(default=0)
    fecha_generacion    = models.DateTimeField(auto_now_add=True)
    version_calculo     = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'analisis_resultados'

    def __str__(self):
        return f"Resultados - Análisis {self.id_analisis_fk.id_analisis}"


class AnalisisArchivos(models.Model):
    id_archivo          = models.AutoField(primary_key=True)
    id_analisis_fk      = models.ForeignKey(
                              Analisis,
                              on_delete=models.CASCADE,
                              related_name='archivos'
                          )
    contenido_json      = models.JSONField()
    version             = models.PositiveIntegerField(default=1)
    activo              = models.BooleanField(default=True)
    es_resultado_modelo = models.BooleanField(
                              default=True,
                              help_text="True = salida automática, False = edición humana"
                          )
    usuario_creacion    = models.ForeignKey(
                              User,
                              on_delete=models.SET_NULL,
                              null=True,
                              blank=True
                          )
    fecha_creacion      = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'analisis_archivos'
        ordering = ['-version']
        unique_together = [['id_analisis_fk', 'version']]
        indexes = [
            GinIndex(fields=['contenido_json'], name='gin_contenido_json'),
            models.Index(fields=['id_analisis_fk'], name='idx_archivo_analisis'),
            models.Index(
                fields=['id_analisis_fk'],
                name='idx_archivo_activo',
                condition=Q(activo=True)
            )
        ]

    def __str__(self):
        return f"Análisis {self.id_analisis_fk.id_analisis} - v{self.version}"
    
    def save(self, *args, **kwargs):
        if not self.pk:
            last_version = AnalisisArchivos.objects.filter(
                id_analisis_fk=self.id_analisis_fk
            ).aggregate(models.Max('version'))['version__max'] or 0
            self.version = last_version + 1
        
        if self.activo:
            AnalisisArchivos.objects.filter(
                id_analisis_fk=self.id_analisis_fk,
                activo=True
            ).update(activo=False)

        super().save(*args, **kwargs)


# ============================================================================
# JOB DE ANÁLISIS
# ============================================================================

class AnalisisJob(models.Model):
    ESTADO_CHOICES = [
        ('pendiente',  'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('completado', 'Completado'),
        ('error',      'Error'),
    ]

    id_job          = models.AutoField(primary_key=True)
    id_caso_fk      = models.ForeignKey(
                          CasoClinico,
                          on_delete=models.CASCADE,
                          related_name='jobs'
                      )
    estado          = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    total_imagenes  = models.IntegerField(default=0)
    procesadas      = models.IntegerField(default=0)
    errores         = models.IntegerField(default=0)
    es_reproceso    = models.BooleanField(default=False)
    version_modelo  = models.CharField(max_length=50, default='cellpose-v1')
    mensaje_error   = models.TextField(blank=True, null=True)
    fecha_inicio    = models.DateTimeField(auto_now_add=True)
    fecha_fin       = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'analisis_job'
        ordering = ['-fecha_inicio']

    @property
    def progreso_porcentaje(self):
        if self.total_imagenes == 0:
            return 0
        return round((self.procesadas / self.total_imagenes) * 100)

    def __str__(self):
        return f"Job {self.id_job} | Caso {self.id_caso_fk_id} | {self.estado} ({self.progreso_porcentaje}%)"