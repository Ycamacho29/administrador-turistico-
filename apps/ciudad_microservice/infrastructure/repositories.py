from datetime import datetime
from core_models.models.Ciudad import Ciudad
from core_models.models.Pais import Pais
from django.core.exceptions import ObjectDoesNotExist


class CiudadRepository:
    """
    Implementación del repositorio usando el ORM de Django.
    Esta capa aísla la lógica de negocio de la base de datos.
    """

    def guardar_ciudad(self, datos: dict) -> Ciudad:
        """
        Realiza la persistencia física de una nueva ciudad en la base de datos.

        Esta es una implementación técnica que utiliza el ORM de Django para 
        insertar un registro en la tabla 'ciudades'. Actúa como el adaptador 
        final entre los datos de la aplicación y el motor de base de datos.
        """
        # 1. Obtenemos la instancia del país
        instancia_pais = Pais.objects.get(id=datos.get('pais_id'))

        # 2. Guardamos la nueva ciudad
        nueva_ciudad = Ciudad.objects.create(
            nombre=datos.get('nombre_ciudad'),
            pais_id=instancia_pais
        )

        return nueva_ciudad

    def obtener_por_id(self, ciudad_id: int) -> Ciudad:
        """Busca una ciudad por su clave primaria."""
        try:
            return Ciudad.objects.get(id=ciudad_id)
        except Ciudad.DoesNotExist:
            return None

    def listar_todas(self):
        """Retorna un QuerySet con todas las ciudades."""
        return Ciudad.objects.all().order_by('-id')

    def actualizar_ciudad(self, ciudad_id: int, datos: dict) -> Ciudad:
        """Actualiza los campos de una ciudad existente."""
        ciudad = Ciudad.objects.get(id=ciudad_id)
        pais = Pais.objects.get(id=datos.get('pais_id'))

        # Actualizamos los campos
        ciudad.nombre = datos.get('nombre_ciudad')
        ciudad.estatus = datos.get('estatus')
        ciudad.pais_id = pais
        ciudad.modificado_en = datetime.now()

        ciudad.save()
        return ciudad

    def eliminar_ciudad(self, ciudad_id: int) -> bool:
        """Elimina una ciudad y retorna True si tuvo éxito."""
        try:
            ciudad = Ciudad.objects.get(id=ciudad_id)
            ciudad.delete()
            return True
        except Ciudad.DoesNotExist:
            return False
