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
    path("socios_y_personas/<int:natillera_id>/", views.personas_y_socios, name="socios_y_personas"),
    
]
