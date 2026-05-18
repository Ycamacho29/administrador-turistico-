from apps.ciudad_microservice.domain.entities.response import ResponseDTO


class PaqueteturisticoServicioUseCases:
    def __init__(self, repository):
        """
        Inyectamos el repositorio para que el caso de uso 
        no dependa de una base de datos específica.
        """
        self.repository = repository

    def create_relacion_servicio_paqueteTuristico(self, request_dto) -> ResponseDTO:
        '''Ejecuta la lógica de negocio para relacionar un Servicio con un Paquete Turistico'''
        try:
            # Lógica de negocio
            datos = request_dto.data

            nueva_relacion_servicio_paqueteTuristico = self.repository.guardar_relacion_servicio_paqueteTuristico(
                datos)

            return ResponseDTO.success(
                data={
                    "id": nueva_relacion_servicio_paqueteTuristico.id,
                    "paquete_turistico": nueva_relacion_servicio_paqueteTuristico.paquete_turistico_id.id,
                    "servico": nueva_relacion_servicio_paqueteTuristico.servico_id.id,
                },
                mensaje="Se relaciono exitosamente el Servicio con el Paquete Turistico"
            )
        except Exception as e:
            return ResponseDTO.error(str(e))

    def get_servicios_x_paqueteTuristico(self, paquete_turistico_id: int) -> ResponseDTO:
        # 1. Consultamos TODAS las relaciones de la tabla puente para este paquete
        relaciones = self.repository.filtrar_por_paquete(paquete_turistico_id)

        # Si la lista viene vacía, el paquete no existe o no tiene servicios vinculados
        if not relaciones:
            return ResponseDTO.error("El Paquete Turístico no tiene ningún servicio asociado", "404")

        # 2. Tomamos la primera fila de la lista para extraer los datos fijos del Paquete
        primera_relacion = relaciones[0]
        paquete = primera_relacion.paquete_turistico_id

        # 3. Recorremos todas las relaciones para extraer únicamente los servicios
        lista_servicios = []
        for relacion in relaciones:
            servicio = relacion.servico_id
            lista_servicios.append({
                "id_relacion_puente": relacion.id,
                "id": servicio.id,
                "nombre": servicio.nombre,
                "descripcion": servicio.descripcion,
                "costo_bs": servicio.costo_bs,
                "estatus": servicio.estatus,
                "creado_en": servicio.creado_en,
                "modificado_en": servicio.modificado_en
            })

        # 4. Construimos la estructura final limpia e integrada
        data = {
            "paquete_turistico": {
                "id": paquete.id,
                "nombre": paquete.nombre,
                "descripcion": paquete.descripcion,
                "destino": {
                    "id": paquete.destino_id.id,
                    "nombre": paquete.destino_id.nombre,
                    "descripcion": paquete.destino_id.descripcion,
                },
                "tipo_paquete": {
                    "id": paquete.tipo_paquete_id.id,
                    "nombre": paquete.tipo_paquete_id.nombre,
                    "descripcion": paquete.tipo_paquete_id.descripcion,
                    "estatus": paquete.tipo_paquete_id.estatus,
                    "creado_en": paquete.tipo_paquete_id.creado_en,
                    "modificado_en": paquete.tipo_paquete_id.modificado_en,
                },
                "duracion_dias": paquete.duracion_dias,
                "precio_base_bs": paquete.precio_base_bs,
                "capacidad_maxima_integrantes": paquete.capacidad_maxima_integrantes,
                "fecha_inico": paquete.fecha_inico,
                "fecha_fin": paquete.fecha_fin,
                "disponible": paquete.disponible,
                "estatus": paquete.estatus,
                "creado_en": paquete.creado_en,
                "modificado_en": paquete.modificado_en
            },
            # Inyectamos la lista completa de servicios aquí
            "servicios": lista_servicios,
        }

        return ResponseDTO.success(data=data)

    # def get_servicios_x_paquetesTuristicos(self) -> ResponseDTO:
    #     clientes = self.repository.listar_todos()
    #     lista_data = [
    #         {
    #             "id": c.id,
    #             "primer_nombre": c.primer_nombre,
    #             "segundo_nombre": c.segundo_nombre,
    #             "primer_apellido": c.primer_apellido,
    #             "segundo_apellido": c.segundo_apellido,
    #             "telefono": c.telefono,
    #             "cedula": c.cedula,
    #             "creado_en": c.creado_en,
    #             "modificado_en": c.modificado_en
    #         }
    #         for c in clientes
    #     ]
    #     return ResponseDTO.success(data=lista_data)

    # def update_servicio_paqueteTuristico(self, relacion_id: int, request_dto) -> ResponseDTO:
    #     try:
    #         # Primero verificamos existencia
    #         relacion_existente = self.repository.obtener_por_id(relacion_id)
    #         if not relacion_existente:
    #             return ResponseDTO.error("Este Servicio no esta Relacionado a este Paquete Turistico", "404")

    #         relacion_actualizada = self.repository.actualizar_relacion_servicio_paqueteTuristico(
    #             relacion_id, request_dto.data)
    #         return ResponseDTO.success(
    #             data={"id": relacion_actualizada.id},
    #             mensaje="Actualizada correctamente"
    #         )
    #     except Exception as e:
    #         return ResponseDTO.error(str(e))

    def delete_servicio_paqueteTuristico(self, cliente_id: int) -> ResponseDTO:
        exito = self.repository.eliminar_relacion_servicio_paqueteTuristico(cliente_id)
        if exito:
            return ResponseDTO.success(mensaje="Eliminado corretamente")
        return ResponseDTO.error("No se pudo eliminar", "400")
