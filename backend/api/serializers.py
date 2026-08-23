from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .models import (
    Doctor,
    Paciente, CasoClinico, Muestra,
    Analisis, AnalisisResultados, AnalisisArchivos,
    AnalisisJob
)

# ============================================================================
# AUTH — Login y perfil
# ============================================================================

class LoginSerializer(serializers.Serializer):
    email    = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email    = data.get('email', '').lower().strip()
        password = data.get('password', '')

        # Django autentica por username; el email lo usamos como username
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('Credenciales inválidas.')

        user = authenticate(username=user_obj.username, password=password)
        if not user:
            raise serializers.ValidationError('Credenciales inválidas.')
        if not user.is_active:
            raise serializers.ValidationError('Esta cuenta está desactivada.')

        # Verificar que tiene perfil de doctor
        if not hasattr(user, 'doctor'):
            raise serializers.ValidationError('Esta cuenta no tiene perfil de doctor.')

        data['user'] = user
        return data


class DoctorSerializer(serializers.ModelSerializer):
    email           = serializers.EmailField(source='user.email', read_only=True)
    nombre_completo = serializers.CharField(read_only=True)
    especialidad_display = serializers.CharField(
        source='get_especialidad_display', read_only=True
    )

    class Meta:
        model  = Doctor
        fields = [
            'id_doctor', 'email', 'nombre', 'apellido',
            'nombre_completo', 'cedula_prof', 'especialidad',
            'especialidad_display', 'institucion', 'telefono',
            'fecha_registro', 'activo',
        ]


class DoctorCreateSerializer(serializers.ModelSerializer):
    """Para crear un doctor con su User asociado."""
    email    = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model  = Doctor
        fields = [
            'email', 'password',
            'nombre', 'apellido', 'cedula_prof',
            'especialidad', 'institucion', 'telefono',
        ]

    def validate_email(self, value):
        value = value.lower().strip()
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Ya existe una cuenta con ese email.')
        return value

    def validate_cedula_prof(self, value):
        if Doctor.objects.filter(cedula_prof=value).exists():
            raise serializers.ValidationError('Ya existe un doctor con esa cédula.')
        return value

    def create(self, validated_data):
        email    = validated_data.pop('email')
        password = validated_data.pop('password')

        # username = parte local del email (único)
        username = email.split('@')[0]
        base_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        doctor = Doctor.objects.create(user=user, **validated_data)
        return doctor


class DoctorUpdateSerializer(serializers.ModelSerializer):
    """Para editar datos del doctor (no email ni contraseña aquí)."""
    class Meta:
        model  = Doctor
        fields = ['nombre', 'apellido', 'cedula_prof', 'especialidad', 'institucion', 'telefono', 'activo']


# ============================================================================
# Demas Tablas
# ============================================================================

class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Paciente
        fields = '__all__'


class CasoClinicoSerializer(serializers.ModelSerializer):
    total_imagenes = serializers.SerializerMethodField()
    
    class Meta:
        model  = CasoClinico
        fields = '__all__'

    def get_total_imagenes(self, obj):
        return obj.muestras.count()


class MuestraSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Muestra
        fields = '__all__'
        extra_kwargs = {
            'fecha_toma': {'required': False},
        }


class AnalisisResultadosSerializer(serializers.ModelSerializer):
    class Meta:
        model  = AnalisisResultados
        fields = '__all__'


class AnalisisArchivosSerializer(serializers.ModelSerializer):
    class Meta:
        model  = AnalisisArchivos
        fields = '__all__'
        read_only_fields = [
            'version', 'activo', 'fecha_creacion', 'usuario_creacion'
        ]


class MuestraMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Muestra
        fields = ['id_muestra', 'ruta_imagen', 'thumbnail', 'tipo_muestra', 'fecha_toma']


class AnalisisSerializer(serializers.ModelSerializer):
    id_muestra_fk = MuestraMiniSerializer(read_only=True)
    resultados    = AnalisisResultadosSerializer(read_only=True)
    archivos      = AnalisisArchivosSerializer(many=True, read_only=True)

    class Meta:
        model  = Analisis
        fields = '__all__'


class AnalisisJobSerializer(serializers.ModelSerializer):
    progreso_porcentaje = serializers.IntegerField(read_only=True)

    class Meta:
        model  = AnalisisJob
        fields = [
            'id_job', 'id_caso_fk', 'estado',
            'total_imagenes', 'procesadas', 'errores',
            'progreso_porcentaje', 'es_reproceso',
            'version_modelo', 'mensaje_error',
            'fecha_inicio', 'fecha_fin',
        ]
        read_only_fields = [
            'estado', 'total_imagenes', 'procesadas', 'errores',
            'progreso_porcentaje', 'mensaje_error', 'fecha_inicio', 'fecha_fin',
        ]