from datetime import datetime
from core_models.models.Pago import Pago
from core_models.models.MetodoPago import MetodoPago
from core_models.models.EstatusPago import EstatusPago
from core_models.models.Moneda import Moneda
from django.core.exceptions import ObjectDoesNotExist


class PagoRepository:
    """
    Implementación del repositorio usando el ORM de Django.
    Esta capa aísla la lógica de negocio de la base de datos.
    """

    def guardar_pago(self, datos: dict, archivo_imagen=None) -> Pago:
        """
        Realiza la persistencia física de una nueva ciudad en la base de datos.

        Esta es una implementación técnica que utiliza el ORM de Django para 
        insertar un registro en la tabla 'ciudades'. Actúa como el adaptador 
        final entre los datos de la aplicación y el motor de base de datos.
        """
        # 1. Obtenemos la instancia de las relaciones con otras tablas
        instancia_metodo_pago = MetodoPago.objects.get(id=datos.get('metodo_pago_id'))
        instancia_estatus_pago = EstatusPago.objects.get(id=datos.get('estatus_pago_id'))
        instancia_moneda = Moneda.objects.get(id=datos.get('moneda_id'))

        # 2. Guardamos el nuevo pago
        nuevo_pago = Pago.objects.create(
            metodo_pago_id=instancia_metodo_pago,
            estatus_pago_id=instancia_estatus_pago,
            moneda_id=instancia_moneda,
            monto_bs=datos.get('monto_bs'),
            monto_otra_moneda=datos.get('monto_otra_moneda'),
            taza_bs=datos.get('taza_bs'),
            comprobante=archivo_imagen
        )

        return nuevo_pago

    def obtener_por_id(self, pago_id: int) -> Pago:
        """Busca un pago por su clave primaria."""
        try:
            return Pago.objects.get(id=pago_id)
        except Pago.DoesNotExist:
            return None

    def listar_todos(self):
        """Retorna un QuerySet con todos los pagos"""
        return Pago.objects.all().order_by('-id')

    def actualizar_pago(self, pago_id: int, datos: dict, archivo_imagen=None) -> Pago:
        """Actualiza los campos de un pago existente"""
        pago = Pago.objects.get(id=pago_id)
        metodo_pago = MetodoPago.objects.get(id=datos.get('metodo_pago_id'))
        estatus_pago = EstatusPago.objects.get(id=datos.get('estatus_pago_id'))
        moneda = Moneda.objects.get(id=datos.get('moneda_id'))

        # Actualizamos los campos
        pago.metodo_pago_id = metodo_pago
        pago.estatus_pago_id = estatus_pago
        pago.moneda_id = moneda
        pago.monto_bs = datos.get('monto_bs')
        pago.monto_otra_moneda = datos.get('monto_otra_moneda')
        pago.taza_bs = datos.get('taza_bs')
        pago.modificado_en = datetime.now()

        if archivo_imagen:
            pago.comprobante = archivo_imagen

        pago.save()
        return pago

    # def eliminar_pago(self, pago_id: int) -> bool:
    #     """Elimina un pago y retorna True si tuvo éxito."""
    #     try:
    #         pago = Pago.objects.get(id=pago_id)
    #         pago.delete()
    #         return True
    #     except Pago.DoesNotExist:
    #         return False
