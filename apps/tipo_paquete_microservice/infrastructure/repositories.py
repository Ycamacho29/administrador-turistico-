from datetime import datetime
from core_models.models.TipoPaquete import TipoPaquete
from django.core.exceptions import ObjectDoesNotExist


class TipoPaqueteRepository:
    """
    Implementación del repositorio usando el ORM de Django.
    Esta capa aísla la lógica de negocio de la base de datos.
    """

    def guardar_tipo_paquete(self, datos: dict) -> TipoPaquete:
        """
        Realiza la persistencia física de un nuevo tipo de paquete en la base de datos.

        Esta es una implementación técnica que utiliza el ORM de Django para 
        insertar un registro en la tabla 'ciudades'. Actúa como el adaptador 
        final entre los datos de la aplicación y el motor de base de datos.
        """

        # Guardamos el nuevo tipo paquete
        nuevo_tipo_paquete = TipoPaquete.objects.create(
            nombre=datos.get('nombre_tipo_paquete'),
            descripcion=datos.get('descripcion')
        )

        return nuevo_tipo_paquete

    def obtener_por_id(self, tipo_paquete_id: int) -> TipoPaquete:
        """Busca un tipo de paquete por su clave primaria."""
        try:
            return TipoPaquete.objects.get(id=tipo_paquete_id)
        except TipoPaquete.DoesNotExist:
            return None

    def listar_todos(self):
        """Retorna un QuerySet con todos los tipos de paquetes"""
        return TipoPaquete.objects.all().order_by('-id')

    def actualizar_tipo_paquete(self, tipo_paquete_id: int, datos: dict) -> TipoPaquete:
        """Actualiza los campos de un tipo paquete"""
        tipo_paquete = TipoPaquete.objects.get(id=tipo_paquete_id)

        # Actualizamos los campos
        tipo_paquete.nombre = datos.get('nombre_tipo_paquete')
        tipo_paquete.descripcion=datos.get('descripcion')
        tipo_paquete.estatus = datos.get('estatus')
        tipo_paquete.modificado_en = datetime.now()

        tipo_paquete.save()
        return tipo_paquete

    def eliminar_tipo_paquete(self, tipo_paquete_id: int) -> bool:
        """Elimina un tipo de paquete y retorna True si tuvo éxito."""
        try:
            tipo_paquete = TipoPaquete.objects.get(id=tipo_paquete_id)
            tipo_paquete.delete()
            return True
        except TipoPaquete.DoesNotExist:
            return False
