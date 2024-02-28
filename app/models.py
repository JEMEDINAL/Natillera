from django.db import models
from django.core.validators import MaxValueValidator


class User(models.Model):
    nombre = models.CharField(max_length=254)
    apellido = models.CharField(max_length=254)
    correo = models.EmailField(max_length=254, unique=True)
    clave = models.CharField(max_length=254)
    
    def __str__(self):
        return self.nombre

class Natillera(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=256)
    direccion = models.CharField(max_length=256)
    telefono = models.CharField(max_length=256)
    periodicidad = models.CharField(max_length=256)
    codigo = models.IntegerField(validators=[MaxValueValidator(9999)], unique=True)
    
    def __str__(self):
        return self.nombre
    
class Persona(models.Model):
    natillera = models.ForeignKey(Natillera, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=256)
    apellido = models.CharField(max_length=256)
    codigo = models.IntegerField(validators=[MaxValueValidator(99999999)], unique=True)
    
    
    
    def __str__(self):
        return self.nombre
    
    

class Socio(models.Model):
    natillera = models.ForeignKey(Natillera, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=256, default='valor_predeterminado')
    apellido = models.CharField(max_length=256, default='valor_predeterminado')
    periodicidad = models.CharField(max_length=50)
    cuota = models.DecimalField(max_digits=10, decimal_places=2)
    codigos = models.IntegerField(validators=[MaxValueValidator(99999999)], unique=True, default=0) 
    activo = models.BooleanField(default=True)
    pais = models.CharField(max_length=256,blank=True, null=True) 
    departamento = models.CharField(max_length=256,blank=True, null=True)
    ciudad = models.CharField(max_length=256,blank=True, null=True)
    Celular = models.CharField(max_length=20,blank=True, null=True)
    correo = models.CharField(max_length=256,blank=True, null=True)
    capital = models.IntegerField(blank=True, null=True)
    fecha_cuota = models.DateField(blank=True, null=True)
    

    
    
    def __str__(self):
        return self.nombre
    
    
class Prestamo(models.Model):
    socio = models.ForeignKey(Socio,on_delete=models.CASCADE)
    cantidad = models.IntegerField(blank=True, null=True)
    deuda = models.IntegerField(blank=True, null=True)
    cuota = models.IntegerField(blank=True, null=True)
    cantidad_cuotas = models.IntegerField(blank=True, null=True)
    tipo_pretamo = models.CharField(max_length=256,default="nada",blank=True, null=True)
    nota_o_descripcion = models.CharField(max_length=265,default="nada",blank=True, null=True)
       
class Eventos(models.Model):
    natillera = models.ForeignKey(Natillera, on_delete=models.CASCADE)
    nombre_del_evento = models.CharField(max_length=256)
    fecha_inicio = models.DateField()
    descripcion = models.CharField(max_length=256)
    
    def __str__(self):
        return self.nombre_del_evento