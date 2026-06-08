'''Modelo de la Tabla metodos_pago'''

from django.db import models
from simple_history.models import HistoricalRecords

class MetodoPago(models.Model):
    '''Clase que Mapea la Tabla metodos_pago'''

    nombre = models.CharField(max_length=100, blank=False, unique=True)
    estatus = models.CharField(max_length=1, default='A')
    creado_en = models.DateField(auto_now_add=True)
    modificado_en = models.DateField(auto_now=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Metodo_Pago'
        verbose_name_plural = 'Metodos_Pagos'
        db_table = 'metodos_pago'

    def __str__(self):
        return str(self.nombre)
