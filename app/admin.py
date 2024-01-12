from django.contrib import admin
from .models import * 
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'apellido', 'correo', 'clave']
    
    

@admin.register(Natillera)
class NatilleraAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'nombre', 'direccion', 'telefono','periodicidad','codigo']
    

@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ['id', 'natillera', 'nombre', 'apellido', 'codigo']
    
    
@admin.register(Socio)
class SocioAdmin(admin.ModelAdmin):
    list_display = ['id', 'periodicidad','cuota']