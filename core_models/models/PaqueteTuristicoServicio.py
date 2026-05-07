'''Modelo de la Tabla paquetesTuristicos_servicios'''

from django.db import models
from core_models.models.PaqueteTuristico import PaqueteTuristico
from core_models.models.Servicio import Servicio

class PaqueteTuristicoServicio(models.Model):
    '''Clase que Mapea la Tabla paquetesTuristicos_servicios'''

    paquete_turistico_id = models.ForeignKey(PaqueteTuristico, on_delete=models.PROTECT)
    servico_id = models.ForeignKey(Servicio, on_delete=models.PROTECT)
    creado_en = models.DateField(auto_now_add=True)
    modificado_en = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'PaqueteTuristico_Servicio'
        verbose_name_plural = 'PaquetesTuristicos_Servicios'
        db_table = 'paquetesTuristicos_servicios'

    def __str__(self):
        return str(f"{self.paquete_turistico_id.nombre} incluye {self.servico_id.nombre}")
