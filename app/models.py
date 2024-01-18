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

    
    
    def __str__(self):
        return self.nombre