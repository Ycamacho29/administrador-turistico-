from datetime import datetime
from core_models.models.EstatusReserva import EstatusReserva
from django.core.exceptions import ObjectDoesNotExist


class EstatusReservasRepository:
    """
    Implementación del repositorio usando el ORM de Django.
    Esta capa aísla la lógica de negocio de la base de datos.
    """

    def guardar_estatus_reserva(self, datos: dict) -> EstatusReserva:
        """
        Realiza la persistencia física de un nuevo estatus de una reserva en la base de datos.

        Esta es una implementación técnica que utiliza el ORM de Django para 
        insertar un registro en la tabla 'ciudades'. Actúa como el adaptador 
        final entre los datos de la aplicación y el motor de base de datos.
        """

        # Guardamos el nuevo estatus de reserva
        nuevo_estatus_reserva = EstatusReserva.objects.create(
            nombre=datos.get('nombre_estatus_reserva'),
            descripcion=datos.get('descripcion')
        )

        return nuevo_estatus_reserva

    def obtener_por_id(self, estatus_reserva_id: int) -> EstatusReserva:
        """Busca una estatus de reserva por su clave primaria."""
        try:
            return EstatusReserva.objects.get(id=estatus_reserva_id)
        except EstatusReserva.DoesNotExist:
            return None

    def listar_todos(self):
        """Retorna un QuerySet con todos los estatus de reserva"""
        return EstatusReserva.objects.all().order_by('-id')

    def actualizar_estatus_reserva(self, estatus_reserva_id: int, datos: dict) -> EstatusReserva:
        """Actualiza los campos de un estatus de reserva existente"""
        estatus_reserva = EstatusReserva.objects.get(id=estatus_reserva_id)

        # Actualizamos los campos
        estatus_reserva.nombre = datos.get('nombre_estatus_reserva')
        estatus_reserva.estatus = datos.get('estatus')
        estatus_reserva.descripcion = datos.get('descripcion')
        estatus_reserva.modificado_en = datetime.now()

        estatus_reserva.save()
        return estatus_reserva

    def eliminar_estatus_reserva(self, estatus_reserva_id: int) -> bool:
        """Elimina un estatus de reserva y retorna True si tuvo éxito."""
        try:
            estatus_reserva = EstatusReserva.objects.get(id=estatus_reserva_id)
            estatus_reserva.delete()
            return True
        except EstatusReserva.DoesNotExist:
            return False
