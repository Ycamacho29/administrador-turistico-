from apps.ciudad_microservice.domain.entities.response import ResponseDTO


class ClienteUseCases:
    def __init__(self, repository):
        """
        Inyectamos el repositorio para que el caso de uso 
        no dependa de una base de datos específica.
        """
        self.repository = repository

    def create_cliente(self, request_dto) -> ResponseDTO:
        '''Ejecuta la lógica de negocio para el registro de un nuevo Cliente'''
        try:
            # Lógica de negocio
            datos = request_dto.data

            nuevo_cliente = self.repository.guardar_cliente(datos)

            return ResponseDTO.success(
                data={
                    "id": nuevo_cliente.id,
                    "primer_nombre": nuevo_cliente.primer_nombre,
                    "segundo_nombre": nuevo_cliente.segundo_nombre,
                    "primer_apellido": nuevo_cliente.primer_apellido,
                    "segundo_apellido": nuevo_cliente.segundo_apellido
                },
                mensaje="Cliente creado exitosamente"
            )
        except Exception as e:
            return ResponseDTO.error(str(e))

    def get_cliente(self, user_id: int) -> ResponseDTO:
        cliente = self.repository.obtener_por_id(user_id)
        if not cliente:
            return ResponseDTO.error("Cliente no encontrado", "404")

        data = {
            "user": {
                "id": cliente.user.id,
            },
            "id": cliente.id,
            "primer_nombre": cliente.primer_nombre,
            "segundo_nombre": cliente.segundo_nombre,
            "primer_apellido": cliente.primer_apellido,
            "segundo_apellido": cliente.segundo_apellido,
            "telefono": cliente.telefono,
            "cedula": cliente.cedula,
            "creado_en": cliente.creado_en,
            "modificado_en": cliente.modificado_en
        }
        return ResponseDTO.success(data=data)

    def get_clientes(self) -> ResponseDTO:
        clientes = self.repository.listar_todos()
        lista_data = [
            {
                "user": {
                    "id": c.user.id,
                    "username": c.user.username,
                    "email": c.user.email,
                },
                "id": c.id,
                "primer_nombre": c.primer_nombre,
                "segundo_nombre": c.segundo_nombre,
                "primer_apellido": c.primer_apellido,
                "segundo_apellido": c.segundo_apellido,
                "telefono": c.telefono,
                "cedula": c.cedula,
                "creado_en": c.creado_en,
                "modificado_en": c.modificado_en
            }
            for c in clientes
        ]
        return ResponseDTO.success(data=lista_data)

    def update_cliente(self, cliente_id: int, request_dto) -> ResponseDTO:
        try:
            # Primero verificamos existencia
            cliente_existente = self.repository.obtener_por_id(cliente_id)
            if not cliente_existente:
                return ResponseDTO.error("Cliente no encontrado para actualizar", "404")

            cliente_actualizado = self.repository.actualizar_cliente(cliente_id, request_dto.data)
            return ResponseDTO.success(
                data={"id": cliente_actualizado.id},
                mensaje="Cliente actualizado correctamente"
            )
        except Exception as e:
            return ResponseDTO.error(str(e))

    def delete_cliente(self, cliente_id: int) -> ResponseDTO:
        exito = self.repository.eliminar_cliente(cliente_id)
        if exito:
            return ResponseDTO.success(mensaje="Cliente eliminado")
        return ResponseDTO.error("No se pudo eliminar el Cliente", "400")
