'''Modelo de la Tabla pagos'''


from django.db import models
from core_models.models.EstatusPago import EstatusPago
from core_models.models.MetodoPago import MetodoPago
from core_models.models.Moneda import Moneda
from core_models.utils import generar_codigo_pago

class Pago(models.Model):
    '''Clase que Mapea la Tabla pagos'''

    codigo_referencia = models.CharField(max_length=12, default=generar_codigo_pago, unique=True, editable=False, db_index=True)
    metodo_pago_id = models.ForeignKey(MetodoPago, on_delete=models.PROTECT)
    estatus_pago_id = models.ForeignKey(EstatusPago, on_delete=models.PROTECT)
    moneda_id = models.ForeignKey(Moneda, on_delete=models.PROTECT)
    monto_bs = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    monto_otra_moneda = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    taza_bs = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    comprobante = models.TextField(blank=False)
    creado_en = models.DateField(auto_now_add=True)
    modificado_en = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
        db_table = 'pagos'

    def __str__(self):
        return str(f"Pago: {self.codigo_referencia} - Metodo Pago: {self.metodo_pago_id.nombre} - {self.estatus_pago_id.nombre}")
