from datetime import datetime
from core_models.models.PaqueteTuristico import PaqueteTuristico
from core_models.models.DestinoTuristico import DestinoTuristico
from core_models.models.TipoPaquete import TipoPaquete
from django.core.exceptions import ObjectDoesNotExist


class PaqueteTuristicoRepository:
    """
    Implementación del repositorio usando el ORM de Django.
    Esta capa aísla la lógica de negocio de la base de datos.
    """

    def guardar_paquete_turistico(self, datos: dict, archivo_imagen=None) -> PaqueteTuristico:
        """
        Realiza la persistencia física de un nuevo Paquete Turistico en la base de datos.

        Esta es una implementación técnica que utiliza el ORM de Django para 
        insertar un registro en la tabla 'paises'. Actúa como el adaptador 
        final entre los datos de la aplicación y el motor de base de datos.
        """
        instancia_destino_turistico = DestinoTuristico.objects.get(id=datos.get('destino_id'))
        instancia_tipo_paquete = TipoPaquete.objects.get(id=datos.get('tipo_paquete_id'))

        # Guardamos el nuevo Paquete Turistico
        nuevo_paquete_turistico = PaqueteTuristico.objects.create(
            nombre=datos.get('nombre_paquete_turistico'),
            descripcion=datos.get('descripcion'),
            destino_id=instancia_destino_turistico,
            tipo_paquete_id=instancia_tipo_paquete,
            duracion_dias=datos.get('duracion_dias'),
            precio_base_bs=datos.get('precio_base_bs'),
            capacidad_maxima_integrantes=datos.get('capacidad_maxima_integrantes'),
            fecha_inico=datos.get('fecha_inico'),
            fecha_fin=datos.get('fecha_fin'),
            imagen_principal=archivo_imagen
        )

        return nuevo_paquete_turistico

    def obtener_por_id(self, paquete_turistico_id: int) -> PaqueteTuristico:
        """Busca un Paquete Turistico por su clave primaria."""

        try:
            return PaqueteTuristico.objects.get(id=paquete_turistico_id)
        except PaqueteTuristico.DoesNotExist:
            return None

    def listar_todos(self):
        """Retorna un QuerySet con todos los Paquetes Turisticos"""
        return PaqueteTuristico.objects.all().order_by('-id')

    def actualizar_paquete_turistico(self, paquete_turistico_id: int, datos: dict, archivo_imagen=None) -> PaqueteTuristico:
        """Actualiza los campos de un paquete turistico existente."""
        instancia_destino_turistico = DestinoTuristico.objects.get(id=datos.get('destino_id'))
        instancia_tipo_paquete = TipoPaquete.objects.get(id=datos.get('tipo_paquete_id'))

        paquete_turistico = PaqueteTuristico.objects.get(id=paquete_turistico_id)

        # Actualizamos los campos
        paquete_turistico.nombre = datos.get('nombre_paquete_turistico')
        paquete_turistico.descripcion = datos.get('descripcion')
        paquete_turistico.destino_id = instancia_destino_turistico
        paquete_turistico.tipo_paquete_id = instancia_tipo_paquete
        paquete_turistico.duracion_dias = datos.get('duracion_dias')
        paquete_turistico.precio_base_bs = datos.get('precio_base_bs')
        paquete_turistico.capacidad_maxima_integrantes = datos.get('capacidad_maxima_integrantes')
        paquete_turistico.fecha_inico = datos.get('fecha_inico')
        paquete_turistico.fecha_fin = datos.get('fecha_fin')
        paquete_turistico.disponible = datos.get('disponible')
        paquete_turistico.estatus = datos.get('estatus')
        paquete_turistico.modificado_en = datetime.now()

        if archivo_imagen:
            paquete_turistico.imagen_principal = archivo_imagen

        paquete_turistico.save()
        return paquete_turistico

    def eliminar_paquete_turistico(self, paquete_turistico_id: int) -> bool:
        """Elimina un pais y retorna True si tuvo éxito."""
        try:
            pais = PaqueteTuristico.objects.get(id=paquete_turistico_id)
            pais.delete()
            return True
        except PaqueteTuristico.DoesNotExist:
            return False
