from apps.ciudad_microservice.domain.entities.response import ResponseDTO


class CiudadUseCases:
    def __init__(self, repository):
        """
        Inyectamos el repositorio para que el caso de uso 
        no dependa de una base de datos específica.
        """
        self.repository = repository

    def create_ciudad(self, request_dto) -> ResponseDTO:
        '''Ejecuta la lógica de negocio para el registro de una nueva ciudad.'''
        try:
            # Lógica de negocio (ej. validar que no exista el nombre)
            datos = request_dto.data

            nueva_ciudad = self.repository.guardar_ciudad(datos)

            return ResponseDTO.success(
                data={
                    "id": nueva_ciudad.id,
                    "nombre": nueva_ciudad.nombre
                },
                mensaje="Ciudad creada exitosamente"
            )
        except Exception as e:
            return ResponseDTO.error(str(e))

    def get_ciudad(self, ciudad_id: int) -> ResponseDTO:
        ciudad = self.repository.obtener_por_id(ciudad_id)
        if not ciudad:
            return ResponseDTO.error("Ciudad no encontrada", "404")

        data = {
            "id": ciudad.id,
            "nombre": ciudad.nombre,
            "pais": {
                "id": ciudad.pais_id.id,
                "nombre": ciudad.pais_id.nombre,
                "estatus": ciudad.pais_id.estatus,
                "creado_en": ciudad.pais_id.creado_en,
                "modificado_en": ciudad.modificado_en,
            },
            "estatus": ciudad.estatus,
            "creado_en": ciudad.creado_en,
            "modificado_en": ciudad.modificado_en
        }
        return ResponseDTO.success(data=data)

    def get_ciudades(self) -> ResponseDTO:
        ciudades = self.repository.listar_todas()
        lista_data = [
            {
                "id": c.id,
                "nombre": c.nombre,
                "pais": {
                    "id": c.pais_id.id,
                    "nombre": c.pais_id.nombre,
                    "estatus": c.pais_id.estatus,
                    "creado_en": c.pais_id.creado_en,
                    "modificado_en": c.modificado_en,
                },
                "estatus": c.estatus,
                "creado_en": c.creado_en,
                "modificado_en": c.modificado_en
            }
            for c in ciudades
        ]
        return ResponseDTO.success(data=lista_data)

    def update_ciudad(self, ciudad_id: int, request_dto) -> ResponseDTO:
        try:
            # Primero verificamos existencia
            ciudad_existente = self.repository.obtener_por_id(ciudad_id)
            if not ciudad_existente:
                return ResponseDTO.error("Ciudad no encontrada para actualizar", "404")

            ciudad_actualizada = self.repository.actualizar_ciudad(
                ciudad_id, request_dto.data)
            return ResponseDTO.success(
                data={"id": ciudad_actualizada.id},
                mensaje="Ciudad actualizada correctamente"
            )
        except Exception as e:
            return ResponseDTO.error(str(e))

    def delete_ciudad(self, ciudad_id: int) -> ResponseDTO:
        exito = self.repository.eliminar_ciudad(ciudad_id)
        if exito:
            return ResponseDTO.success(mensaje="Ciudad eliminada")
        return ResponseDTO.error("No se pudo eliminar la ciudad", "400")
