from apps.ciudad_microservice.domain.entities.response import ResponseDTO


class DestinoTuristicoUseCases:
    def __init__(self, repository):
        """
        Inyectamos el repositorio para que el caso de uso 
        no dependa de una base de datos específica.
        """
        self.repository = repository

    def create_destino_turistico(self, request_dto) -> ResponseDTO:
        '''Ejecuta la lógica de negocio para el registro de un nuevo destino turistico'''
        try:
            # Lógica de negocio
            datos = request_dto.data

            nuevo_destino_turistico = self.repository.guardar_destino_turistico(datos)

            return ResponseDTO.success(
                data={
                    "id": nuevo_destino_turistico.id,
                    "nombre": nuevo_destino_turistico.nombre
                },
                mensaje="Destino Turisrico creado exitosamente"
            )
        except Exception as e:
            return ResponseDTO.error(str(e))

    def get_destino_turistico(self, destino_turistico_id: int) -> ResponseDTO:
        destino_turistico = self.repository.obtener_por_id(destino_turistico_id)
        if not destino_turistico:
            return ResponseDTO.error("Destino Turistico no encontrado", "404")

        data = {
            "id": destino_turistico.id,
            "nombre": destino_turistico.nombre,
            "descripcion": destino_turistico.descripcion,
            "pais": {
                "id": destino_turistico.pais_id.id,
                "nombre": destino_turistico.pais_id.nombre,
                "estatus": destino_turistico.pais_id.estatus,
                "creado_en": destino_turistico.pais_id.creado_en,
                "modificado_en": destino_turistico.pais_id.modificado_en,
            },
            "ciudad": {
                "id": destino_turistico.ciudad_id.id,
                "nombre": destino_turistico.ciudad_id.nombre,
                "estatus": destino_turistico.ciudad_id.estatus,
                "creado_en": destino_turistico.ciudad_id.creado_en,
                "modificado_en": destino_turistico.ciudad_id.modificado_en,
            },
            "idioma_principal": {
                "id": destino_turistico.idioma_principal_id.id,
                "nombre": destino_turistico.idioma_principal_id.nombre,
                "estatus": destino_turistico.idioma_principal_id.estatus,
                "creado_en": destino_turistico.idioma_principal_id.creado_en,
                "modificado_en": destino_turistico.idioma_principal_id.modificado_en,
            },
            "moneda_local": {
                "id": destino_turistico.moneda_local_id.id,
                "nombre": destino_turistico.moneda_local_id.nombre,
                "acronimo": destino_turistico.moneda_local_id.acronimo,
                "estatus": destino_turistico.moneda_local_id.estatus,
                "creado_en": destino_turistico.moneda_local_id.creado_en,
                "modificado_en": destino_turistico.moneda_local_id.modificado_en,
            },
            "estatus": destino_turistico.estatus,
            "creado_en": destino_turistico.creado_en,
            "modificado_en": destino_turistico.modificado_en
        }
        return ResponseDTO.success(data=data)

    def get_destinos_turisticos(self) -> ResponseDTO:
        destinos_turisticos = self.repository.listar_todos()
        lista_data = [
            {
                "id": dt.id,
                "nombre": dt.nombre,
                "descripcion": dt.descripcion,
                "pais": {
                    "id": dt.pais_id.id,
                    "nombre": dt.pais_id.nombre,
                    "estatus": dt.pais_id.estatus,
                    "creado_en": dt.pais_id.creado_en,
                    "modificado_en": dt.pais_id.modificado_en,
                },
                "ciudad": {
                    "id": dt.ciudad_id.id,
                    "nombre": dt.ciudad_id.nombre,
                    "estatus": dt.ciudad_id.estatus,
                    "creado_en": dt.ciudad_id.creado_en,
                    "modificado_en": dt.ciudad_id.modificado_en,
                },
                "idioma_principal": {
                    "id": dt.idioma_principal_id.id,
                    "nombre": dt.idioma_principal_id.nombre,
                    "estatus": dt.idioma_principal_id.estatus,
                    "creado_en": dt.idioma_principal_id.creado_en,
                    "modificado_en": dt.idioma_principal_id.modificado_en,
                },
                "moneda_local": {
                    "id": dt.moneda_local_id.id,
                    "nombre": dt.moneda_local_id.nombre,
                    "acronimo": dt.moneda_local_id.acronimo,
                    "estatus": dt.moneda_local_id.estatus,
                    "creado_en": dt.moneda_local_id.creado_en,
                    "modificado_en": dt.moneda_local_id.modificado_en,
                },
                "estatus": dt.estatus,
                "creado_en": dt.creado_en,
                "modificado_en": dt.modificado_en
            }
            for dt in destinos_turisticos
        ]
        return ResponseDTO.success(data=lista_data)

    def update_destino_turistico(self, destino_turistico_id: int, request_dto) -> ResponseDTO:
        try:
            # Primero verificamos existencia
            destino_turistico_existente = self.repository.obtener_por_id(destino_turistico_id)
            if not destino_turistico_existente:
                return ResponseDTO.error("Destino Turistico no encontrado para actualizar", "404")

            destino_turistico_actualizado = self.repository.actualizar_destino_turistico(
                destino_turistico_id, request_dto.data)
            return ResponseDTO.success(
                data={"id": destino_turistico_actualizado.id},
                mensaje="Destino Turistico actualizado correctamente"
            )
        except Exception as e:
            return ResponseDTO.error(str(e))

    def delete_destino_turistico(self, destino_turistico_id: int) -> ResponseDTO:
        exito = self.repository.eliminar_destino_turistico(destino_turistico_id)
        if exito:
            return ResponseDTO.success(mensaje="Destino Turistico eliminado")
        return ResponseDTO.error("No se pudo eliminar el Destino Turistico", "400")
