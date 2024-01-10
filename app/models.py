from django.db import models


class User(models.Model):
    nombre = models.CharField(max_length=254)
    apellido = models.CharField(max_length=254)
    correo = models.EmailField(max_length=254, unique=True)
    clave = models.CharField(max_length=254)
    
    def __str__(self):
        return self.nombre
