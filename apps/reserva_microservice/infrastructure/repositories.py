from datetime import datetime
from core_models.models.Reserva import Reserva
from core_models.models.Pago import Pago
from core_models.models.PaqueteTuristico import PaqueteTuristico
from core_models.models.Cliente import Cliente
from core_models.models.EstatusReserva import EstatusReserva
from django.core.exceptions import ObjectDoesNotExist


class ReservaRepository:
    """
    Implementación del repositorio usando el ORM de Django.
    Esta capa aísla la lógica de negocio de la base de datos.
    """

    def guardar_reserva(self, datos: dict) -> Reserva:
        """
        Realiza la persistencia física de una nueva Reserva en la base de datos.

        Esta es una implementación técnica que utiliza el ORM de Django para 
        insertar un registro en la tabla 'ciudades'. Actúa como el adaptador 
        final entre los datos de la aplicación y el motor de base de datos.
        """

        pago_id = datos.get('pago_id')
        instancia_pago = Pago.objects.get(id=pago_id) if pago_id else None

        instancia_paquete_turistico = PaqueteTuristico.objects.get(
            id=datos.get('paquete_id'))
        instancia_cliente = Cliente.objects.get(id=datos.get('cliente_id'))
        instancia_estatus_reserva = EstatusReserva.objects.get(
            id=datos.get('estatus_id'))

        # Guardamos la nueva Reserva
        nueva_reserva = Reserva.objects.create(
            pago_id=instancia_pago,
            paquete_id=instancia_paquete_turistico,
            cliente_id=instancia_cliente,
            cantidad_personas=datos.get('cantidad_personas'),
            estatus_id=instancia_estatus_reserva,
        )

        return nueva_reserva

    def obtener_por_id(self, reserva_id: int) -> Reserva:
        """Busca una Reserva por su clave primaria"""
        try:
            return Reserva.objects.get(id=reserva_id)
        except Reserva.DoesNotExist:
            return None

    def listar_todas(self):
        """Retorna un QuerySet con todas las Reservas"""
        return Reserva.objects.all().order_by('-id')

    def actualizar_reserva(self, reserva_id: int, datos: dict) -> Reserva:
        """Actualiza los campos de una Reserva"""
        instancia_pago = Pago.objects.get(id=datos.get('pago_id'))
        instancia_estatus_reserva = EstatusReserva.objects.get(id=datos.get('estatus_id'))

        reserva = Reserva.objects.get(id=reserva_id)

        # Actualizamos los campos
        reserva.pago_id = instancia_pago
        reserva.estatus_id = instancia_estatus_reserva
        reserva.modificado_en = datetime.now()

        reserva.save()
        return reserva

    def eliminar_reserva(self, reserva_id: int) -> bool:
        """Elimina una Reserva y retorna True si tuvo éxito."""
        try:
            reserva = Reserva.objects.get(id=reserva_id)
            reserva.delete()
            return True
        except Reserva.DoesNotExist:
            return False
