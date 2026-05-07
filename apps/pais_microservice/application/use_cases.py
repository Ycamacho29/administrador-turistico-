from apps.pais_microservice.domain.entities.response import ResponseDTO


class PaisUseCases:
    def __init__(self, repository):
        """
        Inyectamos el repositorio para que el caso de uso 
        no dependa de una base de datos específica.
        """
        self.repository = repository

    def create_pais(self, request_dto) -> ResponseDTO:
        '''Ejecuta la lógica de negocio para el registro de un nuevo pais'''

        try:
            # Lógica de negocio (ej. validar que no exista el nombre)
            datos = request_dto.data

            nuevo_pais = self.repository.guardar_pais(datos)

            return ResponseDTO.success(
                data={
                    "id": nuevo_pais.id,
                    "nombre": nuevo_pais.nombre
                },
                mensaje="Pais creada exitosamente"
            )
        except Exception as e:
            return ResponseDTO.error(str(e))

    def get_pais(self, pais_id: int) -> ResponseDTO:
        '''Ejecuta la lógica de negocio para obtener los datos de un pais por su id'''

        pais = self.repository.obtener_por_id(pais_id)
        if not pais:
            return ResponseDTO.error("Pais no encontrado", "404")

        data = {
            "id": pais.id,
            "nombre": pais.nombre,
            "estatus": pais.estatus,
            "creado_en": pais.creado_en,
            "modificado_en": pais.modificado_en
        }
        return ResponseDTO.success(data=data)

    def get_paises(self) -> ResponseDTO:
        paises = self.repository.listar_todos()
        lista_data = [
            {
                "id": p.id,
                "nombre": p.nombre,
                "estatus": p.estatus,
                "creado_en": p.creado_en,
                "modificado_en": p.modificado_en
            }
            for p in paises
        ]
        return ResponseDTO.success(data=lista_data)

    def update_pais(self, pais_id: int, request_dto) -> ResponseDTO:
        try:
            # Primero verificamos existencia
            pais_existente = self.repository.obtener_por_id(pais_id)

            if not pais_existente:
                return ResponseDTO.error("Pais no encontrado para actualizar", "404")

            pais_actualizado = self.repository.actualizar_pais(pais_id, request_dto.data)
            return ResponseDTO.success(
                data={"id": pais_actualizado.id},
                mensaje="Pais actualizado correctamente"
            )
        except Exception as e:
            return ResponseDTO.error(str(e))

    def delete_pais(self, pais_id: int) -> ResponseDTO:
        exito = self.repository.eliminar_pais(pais_id)

        if exito:
            return ResponseDTO.success(mensaje="Pais eliminado")
        return ResponseDTO.error("No se pudo eliminar el pais", "400")
