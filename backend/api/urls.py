from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    # __ AUTH __
    login_view,
    logout_view,
    me_view,
    DoctorViewSet,
    # __ PACIENTES / CASOS __
    PacienteViewSet,
    CasoClinicoViewSet,
    MuestraViewSet,
    AnalisisViewSet,
    MuestraCreateView,
    # __ MÁSCARAS __
    obtener_mascara_png,
    obtener_json_activo,
    guardar_edicion,
    # __ JOBS __
    iniciar_analisis,
    estado_job,
    job_activo_caso,
    # __ CARACTERIZACIÓN __
    caracterizacion_caso,
)

router = DefaultRouter()
router.register(r'pacientes', PacienteViewSet, basename='paciente')
router.register(r'casos',     CasoClinicoViewSet, basename='caso')
router.register(r'muestras',  MuestraViewSet, basename='muestra')
router.register(r'analisis',  AnalisisViewSet, basename='analisis')

# DoctorViewSet manual (no usa queryset directo de modelo)
doctor_list   = DoctorViewSet.as_view({'get': 'list',     'post': 'create'})
doctor_detail = DoctorViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'})

urlpatterns = [

    # ── Auth ────────────────────────────────────────────────────────────
    path('auth/login/',   login_view,    name='auth-login'),
    path('auth/logout/',  logout_view,   name='auth-logout'),
    path('auth/me/',      me_view,       name='auth-me'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    # ── Doctores (solo admin) ────────────────────────────────────────────
    path('doctores/',      doctor_list,          name='doctor-list'),
    path('doctores/<int:pk>/', doctor_detail,    name='doctor-detail'),

    # ── Máscaras ────────────────────────────────────────────────────────
    path('mascaras/<int:id_analisis>/json/',           obtener_json_activo,  name='analisis-json-activo'),
    path('mascaras/<int:id_analisis>/<str:tipo_mascara>/', obtener_mascara_png, name='obtener-mascara-png'),
    path('analisis/<int:id_analisis>/editar/',         guardar_edicion,      name='guardar-edicion'),
    path('subir-muestra/',                             MuestraCreateView.as_view(), name='subir-muestra'),
    path('casos/<int:id_caso>/caracterizacion/',       caracterizacion_caso, name='caracterizacion-caso'),

    # ── Jobs / Segmentación ─────────────────────────────────────────────
    path('casos/<int:id_caso>/analizar/',   iniciar_analisis, name='iniciar-analisis'),
    path('casos/<int:id_caso>/job-activo/', job_activo_caso,  name='job-activo-caso'),
    path('jobs/<int:job_id>/',             estado_job,        name='estado-job'),

    # ── Router (pacientes, casos, muestras, análisis) ───────────────────
    path('', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)