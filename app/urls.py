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
]
