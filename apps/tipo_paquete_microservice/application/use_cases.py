from apps.ciudad_microservice.domain.entities.response import ResponseDTO


class TipoPaqueteUseCases:
    def __init__(self, repository):
        """
        Inyectamos el repositorio para que el caso de uso 
        no dependa de una base de datos específica.
        """
        self.repository = repository

    def create_tipo_paquete(self, request_dto) -> ResponseDTO:
        '''Ejecuta la lógica de negocio para el registro de un nuevo tipo de paquete'''
        try:
            # Lógica de negocio
            datos = request_dto.data

            nuevo_tipo_paquete = self.repository.guardar_tipo_paquete(datos)

            return ResponseDTO.success(
                data={
                    "id": nuevo_tipo_paquete.id,
                    "nombre": nuevo_tipo_paquete.nombre,
                    "descripcion": nuevo_tipo_paquete.descripcion
                },
                mensaje="Tipo de Paquete creado exitosamente"
            )
        except Exception as e:
            return ResponseDTO.error(str(e))

    def get_tipo_paquete(self, tipo_paquete_id: int) -> ResponseDTO:
        tipo_paquete = self.repository.obtener_por_id(tipo_paquete_id)
        if not tipo_paquete:
            return ResponseDTO.error("Tipo de Paquete no encontrado", "404")

        data = {
            "id": tipo_paquete.id,
            "nombre": tipo_paquete.nombre,
            "descripcion": tipo_paquete.descripcion,
            "estatus": tipo_paquete.estatus,
            "creado_en": tipo_paquete.creado_en,
            "modificado_en": tipo_paquete.modificado_en
        }
        return ResponseDTO.success(data=data)

    def get_tipos_paquetes(self) -> ResponseDTO:
        tipos_paquetes = self.repository.listar_todos()
        lista_data = [
            {
                "id": tp.id,
                "nombre": tp.nombre,
                "descripcion": tp.descripcion,
                "estatus": tp.estatus,
                "creado_en": tp.creado_en,
                "modificado_en": tp.modificado_en
            }
            for tp in tipos_paquetes
        ]
        return ResponseDTO.success(data=lista_data)

    def update_tipo_paquete(self, tipo_paquete_id: int, request_dto) -> ResponseDTO:
        try:
            # Primero verificamos existencia
            tipo_paqute_existente = self.repository.obtener_por_id(tipo_paquete_id)
            if not tipo_paqute_existente:
                return ResponseDTO.error("Tipo de Paquete no encontrado para actualizar", "404")

            tipo_paqute_actualizado = self.repository.actualizar_tipo_paquete(tipo_paquete_id, request_dto.data)
            return ResponseDTO.success(
                data={"id": tipo_paqute_actualizado.id},
                mensaje="Tipo Paqute actualizado correctamente"
            )
        except Exception as e:
            return ResponseDTO.error(str(e))

    def delete_tipo_paquete(self, tipo_paquete_id: int) -> ResponseDTO:
        exito = self.repository.eliminar_tipo_paquete(tipo_paquete_id)
        if exito:
            return ResponseDTO.success(mensaje="Tipo de Paquete eliminado")
        return ResponseDTO.error("No se pudo eliminar el tipo de paquete", "400")
