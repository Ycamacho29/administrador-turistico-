from datetime import datetime
from core_models.models.PaqueteTuristicoServicio import PaqueteTuristicoServicio
from core_models.models.PaqueteTuristico import PaqueteTuristico
from core_models.models.Servicio import Servicio
from django.core.exceptions import ObjectDoesNotExist


class PaqueteturisticoServicioRepository:
    """
    Implementación del repositorio usando el ORM de Django.
    Esta capa aísla la lógica de negocio de la base de datos.
    """

    def guardar_relacion_servicio_paqueteTuristico(self, datos: dict) -> PaqueteTuristicoServicio:
        """
        Realiza la persistencia física de la Relacion de un Servicio con un 
        Paquete Turistico.

        Esta es una implementación técnica que utiliza el ORM de Django para 
        insertar un registro en la tabla 'ciudades'. Actúa como el adaptador 
        final entre los datos de la aplicación y el motor de base de datos.
        """
        instancia_paqute_turistico = PaqueteTuristico.objects.get(id=datos.get('paquete_turistico_id'))
        instancia_servicio = Servicio.objects.get(id=datos.get('servico_id'))


        # Guardamos la nueva relacion
        nuevo_relacion = PaqueteTuristicoServicio.objects.create(
            paquete_turistico_id=instancia_paqute_turistico,
            servico_id=instancia_servicio,
        )

        return nuevo_relacion

    def filtrar_por_paquete(self, paquete_turistico_id: int) -> PaqueteTuristicoServicio:
        """Busca los Servicios de un Paquete Turistico por su clave primaria"""
        try:
            return PaqueteTuristicoServicio.objects.filter(paquete_turistico_id=paquete_turistico_id).select_related(
                'paquete_turistico_id',
                'servico_id'
            )
        except PaqueteTuristicoServicio.DoesNotExist:
            return None
        

    # def listar_todos(self):
    #     """Retorna un QuerySet con todos los Clientes"""
    #     return Cliente.objects.all().order_by('-id')

    # def actualizar_relacion_servicio_paqueteTuristico(self, relacion_id: int, datos: dict) -> PaqueteTuristicoServicio:
    #     """Actualiza los campos de un Cliente"""
    #     relacion = PaqueteTuristicoServicio.objects.get(id=relacion_id)

    #     instancia_paqute_turistico = PaqueteTuristico.objects.get(id=datos.get('paquete_turistico_id'))
    #     instancia_servicio = Servicio.objects.get(id=datos.get('servico_id'))

    #     # Actualizamos los campos
    #     relacion.paquete_turistico_id=instancia_paqute_turistico
    #     relacion.servico_id=instancia_servicio
    #     relacion.modificado_en=datetime.now()

    #     relacion.save()
    #     return relacion

    def eliminar_relacion_servicio_paqueteTuristico(self, relacion_id: int) -> bool:
        """Elimina la Relacion entre un Servicio y un Paquete Turistico"""
        try:
            relacion = PaqueteTuristicoServicio.objects.get(id=relacion_id)
            relacion.delete()
            return True
        except relacion.DoesNotExist:
            return False
