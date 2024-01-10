from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name="logout"),
    path('Registrarse/', views.sign_up, name='Registrarse'),
    path('inicio/', views.iniciar_sesion, name='iniciar'),
]
