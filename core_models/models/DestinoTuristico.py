'''Modelo de la Tabla destinos_turisticos'''

from django.db import models
from simple_history.models import HistoricalRecords
from core_models.models.Pais import Pais
from core_models.models.Ciudad import Ciudad
from core_models.models.Idioma import Idioma
from core_models.models.Moneda import Moneda

class DestinoTuristico(models.Model):
    '''Clase que Mapea la Tabla destinos_turisticos'''

    nombre = models.CharField(max_length=100, blank=False, unique=True)
    descripcion = models.TextField(max_length=255, blank=True)
    pais_id = models.ForeignKey(Pais, on_delete=models.PROTECT)
    ciudad_id = models.ForeignKey(Ciudad, on_delete=models.PROTECT)
    idioma_principal_id = models.ForeignKey(Idioma, on_delete=models.PROTECT)
    moneda_local_id = models.ForeignKey(Moneda, on_delete=models.PROTECT)
    estatus = models.CharField(max_length=1, default='A')
    imagen_principal = models.ImageField(upload_to='destinos-turisticos/', blank=True, null=True)
    creado_en = models.DateField(auto_now_add=True)
    modificado_en = models.DateField(auto_now=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Destino_Turistico'
        verbose_name_plural = 'Destinos_Turisticos'
        db_table = 'destinos_turisticos'

    def __str__(self):
        return str(self.nombre)
