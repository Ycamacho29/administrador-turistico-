from datetime import datetime
from core_models.models.MetodoPago import MetodoPago
from django.core.exceptions import ObjectDoesNotExist


class MotodoPagoRepository:
    """
    Implementación del repositorio usando el ORM de Django.
    Esta capa aísla la lógica de negocio de la base de datos.
    """

    def guardar_metodo_pago(self, datos: dict) -> MetodoPago:
        """
        Realiza la persistencia física de un nuevo metodo de pago en la base de datos.

        Esta es una implementación técnica que utiliza el ORM de Django para 
        insertar un registro en la tabla 'ciudades'. Actúa como el adaptador 
        final entre los datos de la aplicación y el motor de base de datos.
        """

        # Guardamos el nuevo metodo de Pago
        nuevo_metodo_pago = MetodoPago.objects.create(
            nombre=datos.get('nombre_metodo_pago')
        )

        return nuevo_metodo_pago

    def obtener_por_id(self, metodo_pago_id: int) -> MetodoPago:
        """Busca un metodo de pago por su clave primaria."""
        try:
            return MetodoPago.objects.get(id=metodo_pago_id)
        except MetodoPago.DoesNotExist:
            return None

    def listar_todos(self):
        """Retorna un QuerySet con todos los metodos de pago"""
        return MetodoPago.objects.all().order_by('-id')

    def actualizar_metodo_pago(self, metodo_pago_id: int, datos: dict) -> MetodoPago:
        """Actualiza los campos de un metodo de pago existente"""
        metodo_pago = MetodoPago.objects.get(id=metodo_pago_id)

        # Actualizamos los campos
        metodo_pago.nombre = datos.get('nombre_metodo_pago')
        metodo_pago.estatus = datos.get('estatus')
        metodo_pago.modificado_en = datetime.now()

        metodo_pago.save()
        return metodo_pago

    def eliminar_metodo_pago(self, metodo_pago_id: int) -> bool:
        """Elimina un metodo de pago y retorna True si tuvo éxito."""
        try:
            metodo_pago = MetodoPago.objects.get(id=metodo_pago_id)
            metodo_pago.delete()
            return True
        except MetodoPago.DoesNotExist:
            return False
