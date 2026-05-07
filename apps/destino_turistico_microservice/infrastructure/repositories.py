from datetime import datetime
from core_models.models.DestinoTuristico import DestinoTuristico
from core_models.models.Pais import Pais
from core_models.models.Ciudad import Ciudad
from core_models.models.Idioma import Idioma
from core_models.models.Moneda import Moneda
from django.core.exceptions import ObjectDoesNotExist


class DestinoTuristicoRepository:
    """
    Implementación del repositorio usando el ORM de Django.
    Esta capa aísla la lógica de negocio de la base de datos.
    """

    def guardar_destino_turistico(self, datos: dict) -> DestinoTuristico:
        """
        Realiza la persistencia física de un nuevo nuevo destino turistico en la base de datos.

        Esta es una implementación técnica que utiliza el ORM de Django para 
        insertar un registro en la tabla 'ciudades'. Actúa como el adaptador 
        final entre los datos de la aplicación y el motor de base de datos.
        """
        # 1. Obtenemos la instancias para las relaciones
        instancia_pais = Pais.objects.get(id=datos.get('pais_id'))
        instancia_ciudad = Ciudad.objects.get(id=datos.get('ciudad_id'))
        instancia_idioma = Idioma.objects.get(id=datos.get('idioma_id'))
        instancia_moneda = Moneda.objects.get(id=datos.get('moneda_id'))

        # 2. Guardamos el nuevo Destino Turistico
        nuevo_destino_turistico = DestinoTuristico.objects.create(
            nombre=datos.get('nombre_destino_turistico'),
            descripcion=datos.get('descripcion'),
            pais_id=instancia_pais,
            ciudad_id=instancia_ciudad,
            idioma_principal_id=instancia_idioma,
            moneda_local_id=instancia_moneda
        )

        return nuevo_destino_turistico

    def obtener_por_id(self, destino_turistico_id: int) -> DestinoTuristico:
        """Busca un Destino Turistico por su clave primaria"""
        try:
            return DestinoTuristico.objects.get(id=destino_turistico_id)
        except DestinoTuristico.DoesNotExist:
            return None

    def listar_todos(self):
        """Retorna un QuerySet con todos los Destino Turisticos"""
        return DestinoTuristico.objects.all().order_by('-id')

    def actualizar_destino_turistico(self, destino_turistico_id: int, datos: dict) -> DestinoTuristico:
        """Actualiza los campos de un destino turistico"""
        destino_turistico = DestinoTuristico.objects.get(id=destino_turistico_id)

        pais = Pais.objects.get(id=datos.get('pais_id'))
        ciudad = Ciudad.objects.get(id=datos.get('ciudad_id'))
        idioma = Idioma.objects.get(id=datos.get('idioma_id'))
        moneda = Moneda.objects.get(id=datos.get('moneda_id'))

        # Actualizamos los campos
        destino_turistico.nombre = datos.get('nombre_destino_turistico')
        destino_turistico.descripcion = datos.get('descripcion')
        destino_turistico.pais_id = pais
        destino_turistico.ciudad_id = ciudad
        destino_turistico.idioma_principal_id = idioma
        destino_turistico.moneda_local_id = moneda
        destino_turistico.estatus = datos.get('estatus')
        destino_turistico.modificado_en = datetime.now()

        destino_turistico.save()
        return destino_turistico

    def eliminar_destino_turistico(self, destino_turistico_id: int) -> bool:
        """Elimina un Destino Turistico y retorna True si tuvo éxito."""
        try:
            destino_turistico = DestinoTuristico.objects.get(id=destino_turistico_id)
            destino_turistico.delete()
            return True
        except DestinoTuristico.DoesNotExist:
            return False
