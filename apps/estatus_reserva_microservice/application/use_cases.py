from apps.ciudad_microservice.domain.entities.response import ResponseDTO


class EstatusReservaUseCases:
    def __init__(self, repository):
        """
        Inyectamos el repositorio para que el caso de uso 
        no dependa de una base de datos específica.
        """
        self.repository = repository

    def create_estatus_reserva(self, request_dto) -> ResponseDTO:
        '''Ejecuta la lógica de negocio para el registro de un nuevo estatus de reserva'''
        try:
            # Lógica de negocio (ej. validar que no exista el nombre)
            datos = request_dto.data

            nuevo_estatus_reserva = self.repository.guardar_estatus_reserva(datos)

            return ResponseDTO.success(
                data={
                    "id": nuevo_estatus_reserva.id,
                    "nombre": nuevo_estatus_reserva.nombre
                },
                mensaje="Estatus de Reserva creado exitosamente"
            )
        except Exception as e:
            return ResponseDTO.error(str(e))

    def get_estatus_reserva(self, estatus_reserva_id: int) -> ResponseDTO:
        estatus_reserva = self.repository.obtener_por_id(estatus_reserva_id)
        if not estatus_reserva:
            return ResponseDTO.error("Estatus de Reserva no encontrado", "404")

        data = {
            "id": estatus_reserva.id,
            "nombre": estatus_reserva.nombre,
            "descripcion": estatus_reserva.descripcion,
            "estatus": estatus_reserva.estatus,
            "creado_en": estatus_reserva.creado_en,
            "modificado_en": estatus_reserva.modificado_en
        }
        return ResponseDTO.success(data=data)

    def get_estatus_reservas(self) -> ResponseDTO:
        estatus_reserva = self.repository.listar_todos()
        lista_data = [
            {
                "id": er.id,
                "nombre": er.nombre,
                "descripcion": er.descripcion,
                "estatus": er.estatus,
                "creado_en": er.creado_en,
                "modificado_en": er.modificado_en
            }
            for er in estatus_reserva
        ]
        return ResponseDTO.success(data=lista_data)

    def update_estatus_reserva(self, estatus_reserva_id: int, request_dto) -> ResponseDTO:
        try:
            # Primero verificamos existencia
            estatus_reserva_existente = self.repository.obtener_por_id(estatus_reserva_id)
            if not estatus_reserva_existente:
                return ResponseDTO.error("Estatus de Reserva no encontrado para actualizar", "404")

            estatus_reserva_actualizado = self.repository.actualizar_estatus_reserva(estatus_reserva_id, request_dto.data)
            return ResponseDTO.success(
                data={"id": estatus_reserva_actualizado.id},
                mensaje="Estatus de Reserva actualizado correctamente"
            )
        except Exception as e:
            return ResponseDTO.error(str(e))

    def delete_estatus_reserva(self, estatus_reserva_id: int) -> ResponseDTO:
        exito = self.repository.eliminar_estatus_reserva(estatus_reserva_id)
        if exito:
            return ResponseDTO.success(mensaje="Estatus Reserva eliminado")
        return ResponseDTO.error("No se pudo eliminar el estatus de reserva", "400")
