from datetime import datetime
from core_models.models.Moneda import Moneda
from django.core.exceptions import ObjectDoesNotExist


class MonedaRepository:
    """
    Implementación del repositorio usando el ORM de Django.
    Esta capa aísla la lógica de negocio de la base de datos.
    """

    def guardar_moneda(self, datos: dict) -> Moneda:
        """
        Realiza la persistencia física de una nueva moneda en la base de datos.

        Esta es una implementación técnica que utiliza el ORM de Django para 
        insertar un registro en la tabla 'ciudades'. Actúa como el adaptador 
        final entre los datos de la aplicación y el motor de base de datos.
        """

        # Guardamos la nueva ciudad
        nueva_moneda = Moneda.objects.create(
            nombre=datos.get('nombre_moneda'),
            acronimo=datos.get('acronimo'),
        )

        return nueva_moneda

    def obtener_por_id(self, moneda_id: int) -> Moneda:
        """Busca una moneda por su clave primaria."""
        try:
            return Moneda.objects.get(id=moneda_id)
        except Moneda.DoesNotExist:
            return None

    def listar_todas(self):
        """Retorna un QuerySet con todas las monedas"""
        return Moneda.objects.all().order_by('-id')

    def actualizar_moneda(self, moneda_id: int, datos: dict) -> Moneda:
        """Actualiza los campos de una moneda existente."""
        moneda = Moneda.objects.get(id=moneda_id)

        # Actualizamos los campos
        moneda.nombre = datos.get('nombre_moneda')
        moneda.acronimo = datos.get('acronimo')
        moneda.estatus = datos.get('estatus')
        moneda.modificado_en = datetime.now()

        moneda.save()
        return moneda

    def eliminar_moneda(self, moneda_id: int) -> bool:
        """Elimina una moneda y retorna True si tuvo éxito."""
        try:
            ciudad = Moneda.objects.get(id=moneda_id)
            ciudad.delete()
            return True
        except Moneda.DoesNotExist:
            return False
