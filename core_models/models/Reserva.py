'''Modelo de la Tabla reservas'''

from django.db import models
from core_models.models.Pago import Pago
from core_models.models.PaqueteTuristico import PaqueteTuristico
from core_models.models.Cliente import Cliente
from core_models.models.EstatusReserva import EstatusReserva

class Reserva(models.Model):
    '''Clase que Mapea la Tabla reservas'''

    codigo = models.CharField(max_length=100, blank=False, unique=True)
    pago_id = models.ForeignKey(Pago, on_delete=models.PROTECT)
    paquete_id = models.ForeignKey(PaqueteTuristico, on_delete=models.PROTECT)
    cliente_id = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    cantidad_personas = models.IntegerField(null=False)
    estatus_id = models.ForeignKey(EstatusReserva, on_delete=models.PROTECT)
    creado_en = models.DateField(auto_now_add=True)
    modificado_en = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        db_table = 'reservas'

    def __str__(self):
        return str(self.nombre)
