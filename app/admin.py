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
    list_display = ['id', 'natillera','codigos','nombre','apellido','periodicidad','cuota','activo','fecha_cuota','capital','ciudad']
    
    
@admin.register(Eventos)
class EventoAdmin(admin.ModelAdmin):
    list_display = ['id', 'natillera','nombre_del_evento','fecha_inicio']
    
    
    
@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ['id', 'socio','cantidad','deuda','cuota','tipo_pretamo', 'cantidad_cuotas','nota_o_descripcion']