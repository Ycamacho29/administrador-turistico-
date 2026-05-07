from datetime import datetime
from core_models.models.Idioma import Idioma
from django.core.exceptions import ObjectDoesNotExist


class IdiomaRepository:
    """
    Implementación del repositorio usando el ORM de Django.
    Esta capa aísla la lógica de negocio de la base de datos.
    """

    def guardar_idioma(self, datos: dict) -> Idioma:
        """
        Realiza la persistencia física de un nuevo idioma en la base de datos.

        Esta es una implementación técnica que utiliza el ORM de Django para 
        insertar un registro en la tabla 'ciudades'. Actúa como el adaptador 
        final entre los datos de la aplicación y el motor de base de datos.
        """

        # Guardamos la nueva ciudad
        nuevo_idioma = Idioma.objects.create(
            nombre=datos.get('nombre_idioma')
        )

        return nuevo_idioma

    def obtener_por_id(self, idioma_id: int) -> Idioma:
        """Busca un idioma por su clave primaria."""
        try:
            return Idioma.objects.get(id=idioma_id)
        except Idioma.DoesNotExist:
            return None

    def listar_todos(self):
        """Retorna un QuerySet con todos los idiomas"""
        return Idioma.objects.all().order_by('-id')

    def actualizar_idioma(self, idioma_id: int, datos: dict) -> Idioma:
        """Actualiza los campos de un idioma existente."""
        idioma = Idioma.objects.get(id=idioma_id)

        # Actualizamos los campos
        idioma.nombre = datos.get('nombre_idioma')
        idioma.estatus = datos.get('estatus')
        idioma.modificado_en = datetime.now()

        idioma.save()
        return idioma

    def eliminar_idioma(self, idioma_id: int) -> bool:
        """Elimina un idioma y retorna True si tuvo éxito."""
        try:
            ciudad = Idioma.objects.get(id=idioma_id)
            ciudad.delete()
            return True
        except Idioma.DoesNotExist:
            return False
