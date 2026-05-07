from apps.ciudad_microservice.domain.entities.response import ResponseDTO


class MotodoPagoUseCases:
    def __init__(self, repository):
        """
        Inyectamos el repositorio para que el caso de uso 
        no dependa de una base de datos específica.
        """
        self.repository = repository

    def create_metodo_pago(self, request_dto) -> ResponseDTO:
        '''Ejecuta la lógica de negocio para el registro de un nuevo metodo de pago'''
        try:
            # Lógica de negocio
            datos = request_dto.data

            nuevo_metodo_pago = self.repository.guardar_metodo_pago(datos)

            return ResponseDTO.success(
                data={
                    "id": nuevo_metodo_pago.id,
                    "nombre": nuevo_metodo_pago.nombre
                },
                mensaje="Metodo de Pago creado exitosamente"
            )
        except Exception as e:
            return ResponseDTO.error(str(e))

    def get_metodo_pago(self, metodo_pago_id: int) -> ResponseDTO:
        metodo_pago = self.repository.obtener_por_id(metodo_pago_id)
        if not metodo_pago:
            return ResponseDTO.error("Estatus Pago no encontrado", "404")

        data = {
            "id": metodo_pago.id,
            "nombre": metodo_pago.nombre,
            "estatus": metodo_pago.estatus,
            "creado_en": metodo_pago.creado_en,
            "modificado_en": metodo_pago.modificado_en
        }
        return ResponseDTO.success(data=data)

    def get_metodos_pago(self) -> ResponseDTO:
        metodos_pagos = self.repository.listar_todos()
        lista_data = [
            {
                "id": mp.id,
                "nombre": mp.nombre,
                "estatus": mp.estatus,
                "creado_en": mp.creado_en,
                "modificado_en": mp.modificado_en
            }
            for mp in metodos_pagos
        ]
        return ResponseDTO.success(data=lista_data)

    def update_metodo_pago(self, metodo_pago_id: int, request_dto) -> ResponseDTO:
        try:
            # Primero verificamos existencia
            metodo_pago_existente = self.repository.obtener_por_id(metodo_pago_id)
            if not metodo_pago_existente:
                return ResponseDTO.error("Metodo de pago no encontrado para actualizar", "404")

            metodo_pago_actualizado = self.repository.actualizar_metodo_pago(metodo_pago_id, request_dto.data)
            return ResponseDTO.success(
                data={"id": metodo_pago_actualizado.id},
                mensaje="Metodo de Pago actualizado correctamente"
            )
        except Exception as e:
            return ResponseDTO.error(str(e))

    def delete_metodo_pago(self, metodo_pago_id: int) -> ResponseDTO:
        exito = self.repository.eliminar_metodo_pago(metodo_pago_id)
        if exito:
            return ResponseDTO.success(mensaje="Metodo de Pago eliminado")
        return ResponseDTO.error("No se pudo eliminar el Metodo de Pago", "400")
