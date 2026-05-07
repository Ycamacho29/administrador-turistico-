from apps.idioma_microservice.domain.entities.response import ResponseDTO

class IdiomaUseCases:
    def __init__(self, repository):
        """
        Inyectamos el repositorio para que el caso de uso 
        no dependa de una base de datos específica.
        """
        self.repository = repository

    def create_idioma(self, request_dto) -> ResponseDTO:
        '''Ejecuta la lógica de negocio para el registro de un nuevo idioma'''
        try:
            datos = request_dto.data

            nuevo_idioma = self.repository.guardar_idioma(datos)

            return ResponseDTO.success(
                data={
                    "id": nuevo_idioma.id,
                    "nombre": nuevo_idioma.nombre
                },
                mensaje="Idioma creado exitosamente"
            )
        except Exception as e:
            return ResponseDTO.error(str(e))

    def get_idioma(self, idioma_id: int) -> ResponseDTO:
        idioma = self.repository.obtener_por_id(idioma_id)
        if not idioma:
            return ResponseDTO.error("Idioma no encontrado", "404")

        data = {
            "id": idioma.id,
            "nombre": idioma.nombre,
            "estatus": idioma.estatus,
            "creado_en": idioma.creado_en,
            "modificado_en": idioma.modificado_en
        }
        return ResponseDTO.success(data=data)

    def get_idiomas(self) -> ResponseDTO:
        idiomas = self.repository.listar_todos()
        lista_data = [
            {
                "id": i.id,
                "nombre": i.nombre,
                "estatus": i.estatus,
                "creado_en": i.creado_en,
                "modificado_en": i.modificado_en
            }
            for i in idiomas
        ]
        return ResponseDTO.success(data=lista_data)

    def update_idioma(self, idioma_id: int, request_dto) -> ResponseDTO:
        try:
            # Primero verificamos existencia
            idioma_existente = self.repository.obtener_por_id(idioma_id)
            if not idioma_existente:
                return ResponseDTO.error("Idioma no encontrado para actualizar", "404")

            idioma_actualizado = self.repository.actualizar_idioma(idioma_id, request_dto.data)
            return ResponseDTO.success(
                data={"id": idioma_actualizado.id},
                mensaje="Idioma actualizado correctamente"
            )
        except Exception as e:
            return ResponseDTO.error(str(e))

    def delete_idioma(self, idioma_id: int) -> ResponseDTO:
        exito = self.repository.eliminar_idioma(idioma_id)
        if exito:
            return ResponseDTO.success(mensaje="Idioma eliminado")
        return ResponseDTO.error("No se pudo eliminar el idioma", "400")
