'''Modelo de la Tabla clientes'''

from django.db import models


class Cliente(models.Model):
    '''Clase que Mapea la Tabla clientes'''

    primer_nombre = models.CharField(max_length=100, blank=False, unique=False)
    segundo_nombre = models.CharField(max_length=100, blank=True, unique=False)
    primer_apellido = models.CharField(
        max_length=100, blank=False, unique=False)
    segundo_apellido = models.CharField(
        max_length=100, blank=True, unique=False)
    telefono = models.CharField(max_length=12, blank=False, unique=True)
    cedula = models.CharField(max_length=10, blank=False, unique=True)
    creado_en = models.DateField(auto_now_add=True)
    modificado_en = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        db_table = 'clientes'

    def __str__(self):
        return str(f"{self.primer_nombre + self.segundo_nombre + self.primer_apellido + self.segundo_apellido} - Identifiacion:({self.cedula})")
