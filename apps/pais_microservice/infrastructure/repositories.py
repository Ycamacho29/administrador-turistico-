from datetime import datetime
from core_models.models.Pais import Pais
from django.core.exceptions import ObjectDoesNotExist


class PaisRepository:
    """
    Implementación del repositorio usando el ORM de Django.
    Esta capa aísla la lógica de negocio de la base de datos.
    """

    def guardar_pais(self, datos: dict) -> Pais:
        """
        Realiza la persistencia física de un nuevo pais en la base de datos.

        Esta es una implementación técnica que utiliza el ORM de Django para 
        insertar un registro en la tabla 'paises'. Actúa como el adaptador 
        final entre los datos de la aplicación y el motor de base de datos.
        """

        # Guardamos el nuevo pais
        nuevo_pais = Pais.objects.create(
            nombre=datos.get('nombre_pais'),
        )

        return nuevo_pais

    def obtener_por_id(self, pais_id: int) -> Pais:
        """Busca un pais por su clave primaria."""

        try:
            return Pais.objects.get(id=pais_id)
        except Pais.DoesNotExist:
            return None

    def listar_todos(self):
        """Retorna un QuerySet con todos los paises"""
        return Pais.objects.all().order_by('-id')

    def actualizar_pais(self, pais_id: int, datos: dict) -> Pais:
        """Actualiza los campos de un pais existente."""

        pais = Pais.objects.get(id=pais_id)

        # Actualizamos los campos
        pais.nombre = datos.get('nombre_pais')
        pais.estatus = datos.get('estatus')
        pais.modificado_en = datetime.now()

        pais.save()
        return pais

    def eliminar_pais(self, pais_id: int) -> bool:
        """Elimina un pais y retorna True si tuvo éxito."""
        try:
            pais = Pais.objects.get(id=pais_id)
            pais.delete()
            return True
        except Pais.DoesNotExist:
            return False
