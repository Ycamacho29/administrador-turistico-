'''Modelo de la Tabla estatus_reservas'''

from django.db import models
from simple_history.models import HistoricalRecords

class EstatusReserva(models.Model):
    '''Clase que Mapea la Tabla estatus_reservas'''

    nombre = models.CharField(max_length=100, blank=False, unique=True)
    descripcion = models.TextField(max_length=255, blank=True)
    estatus = models.CharField(max_length=1, default='A')
    creado_en = models.DateField(auto_now_add=True)
    modificado_en = models.DateField(auto_now=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Estatus_Reserva'
        verbose_name_plural = 'Estatus_Reservas'
        db_table = 'estatus_reservas'

    def __str__(self):
        return str(f"{self.nombre}")
