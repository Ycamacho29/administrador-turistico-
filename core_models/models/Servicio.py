'''Modelo de la Tabla servicios'''

from django.db import models
from simple_history.models import HistoricalRecords

class Servicio(models.Model):
    '''Clase que Mapea la Tabla servicios'''

    nombre = models.CharField(max_length=100, blank=False, unique=True)
    descripcion = models.TextField(max_length=255, blank=True)
    costo_bs = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    estatus = models.CharField(max_length=1, default='A')
    creado_en = models.DateField(auto_now_add=True)
    modificado_en = models.DateField(auto_now=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'
        db_table = 'servicios'

    def __str__(self):
        return str(f"{self.nombre} - ({self.costo_bs})")
