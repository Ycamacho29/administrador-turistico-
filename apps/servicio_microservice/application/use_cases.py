from apps.ciudad_microservice.domain.entities.response import ResponseDTO


class ServicioUseCases:
    def __init__(self, repository):
        """
        Inyectamos el repositorio para que el caso de uso 
        no dependa de una base de datos específica.
        """
        self.repository = repository

    def create_servicio(self, request_dto) -> ResponseDTO:
        '''Ejecuta la lógica de negocio para el registro de un nuevo servicio'''
        try:
            # Lógica de negocio (ej. validar que no exista el nombre)
            datos = request_dto.data

            nuevo_servicio = self.repository.guardar_servicio(datos)

            return ResponseDTO.success(
                data={
                    "id": nuevo_servicio.id,
                    "nombre": nuevo_servicio.nombre,
                    "descripcion": nuevo_servicio.descripcion,
                    "costo_bs": nuevo_servicio.costo_bs
                },
                mensaje="Servicio creado exitosamente"
            )
        except Exception as e:
            return ResponseDTO.error(str(e))

    def get_servicio(self, servicio_id: int) -> ResponseDTO:
        servicio = self.repository.obtener_por_id(servicio_id)
        if not servicio:
            return ResponseDTO.error("Servicio no encontrado", "404")

        data = {
            "id": servicio.id,
            "nombre": servicio.nombre,
            "descripcion": servicio.descripcion,
            "costo_bs": servicio.costo_bs,
            "estatus": servicio.estatus,
            "creado_en": servicio.creado_en,
            "modificado_en": servicio.modificado_en
        }
        return ResponseDTO.success(data=data)

    def get_servicios(self) -> ResponseDTO:
        servicios = self.repository.listar_todos()
        lista_data = [
            {
                "id": s.id,
                "nombre": s.nombre,
                "descripcion": s.descripcion,
                "costo_bs": s.costo_bs,
                "estatus": s.estatus,
                "creado_en": s.creado_en,
                "modificado_en": s.modificado_en
            }
            for s in servicios
        ]
        return ResponseDTO.success(data=lista_data)

    def update_servicio(self, servicio_id: int, request_dto) -> ResponseDTO:
        try:
            # Primero verificamos existencia
            servicio_existente = self.repository.obtener_por_id(servicio_id)
            if not servicio_existente:
                return ResponseDTO.error("Servicio no encontrado para actualizar", "404")

            servicio_actualizado = self.repository.actualizar_servicio(servicio_id, request_dto.data)
            return ResponseDTO.success(
                data={"id": servicio_actualizado.id},
                mensaje="Servicio actualizado correctamente"
            )
        except Exception as e:
            return ResponseDTO.error(str(e))

    def delete_servicio(self, servicio_id: int) -> ResponseDTO:
        exito = self.repository.eliminar_servicio(servicio_id)
        if exito:
            return ResponseDTO.success(mensaje="Servicio eliminado")
        return ResponseDTO.error("No se pudo eliminar el servicio", "400")
