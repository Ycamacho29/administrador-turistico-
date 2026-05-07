'''Modelo de la Tabla paquetes_turisticos'''

from django.db import models
from core_models.models.DestinoTuristico import DestinoTuristico
from core_models.models.TipoPaquete import TipoPaquete

class PaqueteTuristico(models.Model):
    '''Clase que Mapea la Tabla paquetes_turisticos'''

    nombre = models.CharField(max_length=100, blank=False, unique=True)
    descripcion = models.TextField(max_length=255, blank=True)
    destino_id = models.ForeignKey(DestinoTuristico, on_delete=models.PROTECT)
    tipo_paquete_id = models.ForeignKey(TipoPaquete, on_delete=models.PROTECT)
    duracion_dias = models.IntegerField(null=False)
    precio_base_bs = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    capacidad_maxima_integrantes = models.IntegerField(null=False)
    fecha_inico = models.DateField()
    fecha_fin = models.DateField()
    disponible = models.CharField(max_length=1, default='A')
    estatus = models.CharField(max_length=1, default='A')
    imagen_principal = models.TextField(blank=True)
    creado_en = models.DateField(auto_now_add=True)
    modificado_en = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Paquete_Turistico'
        verbose_name_plural = 'Paquetes_Turisticos'
        db_table = 'paquetes_turisticos'

    def __str__(self):
        return str(self.nombre)
