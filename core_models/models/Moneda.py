'''Modelo de la Tabla monedas'''

from django.db import models


class Moneda(models.Model):
    '''Clase que Mapea la Tabla monedas'''

    nombre = models.CharField(max_length=100, blank=False, unique=True)
    acronimo = models.CharField(max_length=4, blank=False, unique=True)
    estatus = models.CharField(max_length=1, default='A')
    creado_en = models.DateField(auto_now_add=True)
    modificado_en = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Moneda'
        verbose_name_plural = 'Monedas'
        db_table = 'monedas'

    def __str__(self):
        return str(self.nombre)
