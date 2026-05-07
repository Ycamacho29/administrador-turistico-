from apps.ciudad_microservice.domain.entities.response import ResponseDTO


class EstatusPagoUseCases:
    def __init__(self, repository):
        """
        Inyectamos el repositorio para que el caso de uso 
        no dependa de una base de datos específica.
        """
        self.repository = repository

    def create_estatus_pago(self, request_dto) -> ResponseDTO:
        '''Ejecuta la lógica de negocio para el registro de un nuevo estatus de pago'''
        try:
            # Lógica de negocio
            datos = request_dto.data

            nuevo_estatus_pago = self.repository.guardar_estatus_pago(datos)

            return ResponseDTO.success(
                data={
                    "id": nuevo_estatus_pago.id,
                    "nombre": nuevo_estatus_pago.nombre
                },
                mensaje="Estatus de Pago creado exitosamente"
            )
        except Exception as e:
            return ResponseDTO.error(str(e))

    def get_estatus_pago(self, estatus_pago_id: int) -> ResponseDTO:
        estatus_pago = self.repository.obtener_por_id(estatus_pago_id)
        if not estatus_pago:
            return ResponseDTO.error("Estatus Pago no encontrado", "404")

        data = {
            "id": estatus_pago.id,
            "nombre": estatus_pago.nombre,
            "estatus": estatus_pago.estatus,
            "descripcion": estatus_pago.descripcion,
            "creado_en": estatus_pago.creado_en,
            "modificado_en": estatus_pago.modificado_en
        }
        return ResponseDTO.success(data=data)

    def get_estatus_pagos(self) -> ResponseDTO:
        estatus_pagos = self.repository.listar_todos()
        lista_data = [
            {
                "id": ep.id,
                "nombre": ep.nombre,
                "descripcion": ep.descripcion,
                "estatus": ep.estatus,
                "creado_en": ep.creado_en,
                "modificado_en": ep.modificado_en
            }
            for ep in estatus_pagos
        ]
        return ResponseDTO.success(data=lista_data)

    def update_estatus_pago(self, estatus_pago_id: int, request_dto) -> ResponseDTO:
        try:
            # Primero verificamos existencia
            estatus_pago_existente = self.repository.obtener_por_id(estatus_pago_id)
            if not estatus_pago_existente:
                return ResponseDTO.error("Estatus de pago no encontrado para actualizar", "404")

            estatus_pago_actualizado = self.repository.actualizar_estatus_pago(estatus_pago_id, request_dto.data)
            return ResponseDTO.success(
                data={"id": estatus_pago_actualizado.id},
                mensaje="Estatus de Pago actualizado correctamente"
            )
        except Exception as e:
            return ResponseDTO.error(str(e))

    def delete_estatus_pago(self, estatus_pago_id: int) -> ResponseDTO:
        exito = self.repository.eliminar_estatus_pago(estatus_pago_id)
        if exito:
            return ResponseDTO.success(mensaje="Estatus de Pago eliminado")
        return ResponseDTO.error("No se pudo eliminar el Estatus de Pago", "400")
