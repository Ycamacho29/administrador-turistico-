'''Modelo de la Tabla estatus_pagos'''

from django.db import models


class EstatusPago(models.Model):
    '''Clase que Mapea la Tabla estatus_pagos'''

    nombre = models.CharField(max_length=100, blank=False, unique=True)
    descripcion = models.TextField(max_length=255, blank=True)
    estatus = models.CharField(max_length=1, default='A')
    creado_en = models.DateField(auto_now_add=True)
    modificado_en = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Estatus_Pago'
        verbose_name_plural = 'Estatus_pagos'
        db_table = 'estatus_pagos'

    def __str__(self):
        return str(self.nombre)
