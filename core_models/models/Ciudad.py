'''Modelo de la Tabla ciudades'''

from django.db import models
from core_models.models.Pais import Pais


class Ciudad(models.Model):
    '''Clase que Mapea la Tabla ciudades'''

    nombre = models.CharField(max_length=100, blank=False, unique=True)
    estatus = models.CharField(max_length=1, default='A')
    pais_id = models.ForeignKey(Pais, on_delete=models.PROTECT)
    creado_en = models.DateField(auto_now_add=True)
    modificado_en = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Ciudad'
        verbose_name_plural = 'Ciudades'
        db_table = 'ciudades'
        indexes = [
            models.Index(fields=["pais_id"], name='idx_ciudades_pais'),
        ]

    def __str__(self):
        return str(f"{self.nombre} - ({self.pais_id.nombre})")
