'''Modelo de la Tabla tipos_paquetes'''

from django.db import models
from simple_history.models import HistoricalRecords

class TipoPaquete(models.Model):
    '''Clase que Mapea la Tabla tipos_paquetes'''

    nombre = models.CharField(max_length=100, blank=False, unique=True)
    descripcion = models.TextField(max_length=255, blank=True)
    estatus = models.CharField(max_length=1, default='A')
    creado_en = models.DateField(auto_now_add=True)
    modificado_en = models.DateField(auto_now=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Tipo_Paquete'
        verbose_name_plural = 'Tipos_Paquetes'
        db_table = 'tipos_paquetes'

    def __str__(self):
        return str(self.nombre)
