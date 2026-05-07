'''Modelo de la Tabla paises'''

from django.db import models


class Pais(models.Model):
    '''Clase que Mapea la Tabla paises'''

    nombre = models.CharField(max_length=100, blank=False, unique=True)
    estatus = models.CharField(max_length=1, default='A')
    creado_en = models.DateField(auto_now_add=True)
    modificado_en = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Pais'
        verbose_name_plural = 'Paises'
        db_table = 'paises'

    def __str__(self):
        return str(self.nombre)
