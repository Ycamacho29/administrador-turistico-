from datetime import datetime
from core_models.models.EstatusPago import EstatusPago
from django.core.exceptions import ObjectDoesNotExist


class EstatusPagoRepository:
    """
    Implementación del repositorio usando el ORM de Django.
    Esta capa aísla la lógica de negocio de la base de datos.
    """

    def guardar_estatus_pago(self, datos: dict) -> EstatusPago:
        """
        Realiza la persistencia física de un nuevo estatus de pago en la base de datos.

        Esta es una implementación técnica que utiliza el ORM de Django para 
        insertar un registro en la tabla 'ciudades'. Actúa como el adaptador 
        final entre los datos de la aplicación y el motor de base de datos.
        """

        # Guardamos el nuevo Estatus de Pago
        nuevo_estatus_pago = EstatusPago.objects.create(
            nombre=datos.get('nombre_estatus_pago'),
            descripcion=datos.get('descripcion')
        )

        return nuevo_estatus_pago

    def obtener_por_id(self, estatus_pago_id: int) -> EstatusPago:
        """Busca un estatus de pago por su clave primaria."""
        try:
            return EstatusPago.objects.get(id=estatus_pago_id)
        except EstatusPago.DoesNotExist:
            return None

    def listar_todos(self):
        """Retorna un QuerySet con todos los estatus de pago"""
        return EstatusPago.objects.all().order_by('-id')

    def actualizar_estatus_pago(self, estatus_pago_id: int, datos: dict) -> EstatusPago:
        """Actualiza los campos de un estatus de pago existente"""
        estatus_pago = EstatusPago.objects.get(id=estatus_pago_id)

        # Actualizamos los campos
        estatus_pago.nombre = datos.get('nombre_estatus_pago')
        estatus_pago.estatus = datos.get('estatus')
        estatus_pago.descripcion = datos.get('descripcion')
        estatus_pago.modificado_en = datetime.now()

        estatus_pago.save()
        return estatus_pago

    def eliminar_estatus_pago(self, estatus_pago_id: int) -> bool:
        """Elimina un estatus de pago y retorna True si tuvo éxito."""
        try:
            estatus_pago = EstatusPago.objects.get(id=estatus_pago_id)
            estatus_pago.delete()
            return True
        except EstatusPago.DoesNotExist:
            return False
