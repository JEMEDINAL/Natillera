from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name="logout"),
    path('Registrarse/', views.sign_up, name='Registrarse'),
    path('inicio/', views.iniciar_sesion, name='iniciar'),
    path('crear_natillera/', views.crear_natillera, name='crear_natillera'),
    path("listar_natillera/", views.nati_usuario, name="listar"),
    path("propiedad_natillera/<int:natillera_id>/", views.propiedad_natillera, name="propiedad_natillera"),
    path("crear_persona/", views.personas_crear, name="crear_persona"),
    path("crear_socio/", views.socio_crear, name="crear_socio"),
    path("lista_personas/", views.json_personas, name='lista_personas'),
    path("lista_socios/", views.json_socio, name='lista_socios'),
    path("propiedades_socio/<int:socio_id>", views.propiedad_socio, name='propiedades_socio'),
    path("editar_socio/", views.editar_socio, name='editar_socio'),
    path("table_socio/", views.socio_table,name="table_socio"),
    path("dar_cuota/<int:id_socio>", views.dar_couta, name="dar_cuota"),
    path("dar_cuota_form/", views.dar_cuota_form, name="dar_cuota_form"),
    path("calendario/", views.calendario, name="calendario"),
    path("crear_evento/", views.crear_evento, name="crear_evento"),
    path("eliminar_evento/", views.eliminar_evento, name="eliminar_evento"),
    path("prestamos/<int:socio_id>", views.prestamos, name="prestamos"),
    path("crear_prestamos/", views.crear_prestamos, name="crear_prestamos"),
    path("pagar_deuda/<int:id_socio>", views.pagar_deuda, name="pagar_deuda"),
    path("pagar_pagar_deuda/", views.pagar_pagar_deuda, name="pagar_pagar_deuda"),
]
