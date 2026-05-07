from datetime import datetime
from core_models.models.Servicio import Servicio
from django.core.exceptions import ObjectDoesNotExist


class ServicioRepository:
    """
    Implementación del repositorio usando el ORM de Django.
    Esta capa aísla la lógica de negocio de la base de datos.
    """

    def guardar_servicio(self, datos: dict) -> Servicio:
        """
        Realiza la persistencia física de un nuevo servicio en la base de datos.

        Esta es una implementación técnica que utiliza el ORM de Django para 
        insertar un registro en la tabla 'ciudades'. Actúa como el adaptador 
        final entre los datos de la aplicación y el motor de base de datos.
        """

        # Guardamos el nuevo servicio
        nuevo_servicio = Servicio.objects.create(
            nombre=datos.get('nombre_servicio'),
            descripcion=datos.get('descripcion'),
            costo_bs=datos.get('costo_bs')
        )

        return nuevo_servicio

    def obtener_por_id(self, servicio_id: int) -> Servicio:
        """Busca un servicio por su clave primaria."""
        try:
            return Servicio.objects.get(id=servicio_id)
        except Servicio.DoesNotExist:
            return None

    def listar_todos(self):
        """Retorna un QuerySet con todos los servicios"""
        return Servicio.objects.all().order_by('-id')

    def actualizar_servicio(self, servicio_id: int, datos: dict) -> Servicio:
        """Actualiza los campos de un servicio existente."""
        servicio = Servicio.objects.get(id=servicio_id)

        # Actualizamos los campos
        servicio.nombre = datos.get('nombre_servicio')
        servicio.descripcion=datos.get('descripcion')
        servicio.costo_bs=datos.get('costo_bs')
        servicio.estatus = datos.get('estatus')
        servicio.modificado_en = datetime.now()

        servicio.save()
        return servicio

    def eliminar_servicio(self, servicio_id: int) -> bool:
        """Elimina un servicio y retorna True si tuvo éxito."""
        try:
            ciudad = Servicio.objects.get(id=servicio_id)
            ciudad.delete()
            return True
        except Servicio.DoesNotExist:
            return False
