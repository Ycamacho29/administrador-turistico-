from apps.ciudad_microservice.domain.entities.response import ResponseDTO


class PaqueteTuristicoUseCases:
    def __init__(self, repository):
        """
        Inyectamos el repositorio para que el caso de uso 
        no dependa de una base de datos específica.
        """
        self.repository = repository

    def create_paquete_turistico(self, request_dto) -> ResponseDTO:
        '''Ejecuta la lógica de negocio para el registro de un nuevo paquete turistico'''
        try:
            # Lógica de negocio
            datos = request_dto.data

            archivo_imagen = datos.get('imagen_principal', None)

            nuevo_paqutete_turistico = self.repository.guardar_paquete_turistico(datos, archivo_imagen)

            return ResponseDTO.success(
                data={
                    "id": nuevo_paqutete_turistico.id,
                    "nombre": nuevo_paqutete_turistico.nombre
                },
                mensaje="Paquete Turisrico creado exitosamente"
            )
        except Exception as e:
            return ResponseDTO.error(str(e))

    def get_paquete_turistico(self, paquete_turistico_id: int) -> ResponseDTO:
        paquete_turistico_turistico = self.repository.obtener_por_id(paquete_turistico_id)
        if not paquete_turistico_turistico:
            return ResponseDTO.error("Paquete Turistico no encontrado", "404")

        # Construimos la URL pública de la imagen de forma segura si el registro la tiene
        url_imagen = paquete_turistico_turistico.imagen_principal.url if paquete_turistico_turistico.imagen_principal else None

        data = {
            "id": paquete_turistico_turistico.id,
            "nombre": paquete_turistico_turistico.nombre,
            "descripcion": paquete_turistico_turistico.descripcion,
            "imagen_principal": url_imagen,
            "destino": {
                "id": paquete_turistico_turistico.destino_id.id,
                "nombre": paquete_turistico_turistico.destino_id.nombre,
                "descripcion": paquete_turistico_turistico.destino_id.descripcion,
            },
            "tipo_paquete": {
                "id": paquete_turistico_turistico.tipo_paquete_id.id,
                "nombre": paquete_turistico_turistico.tipo_paquete_id.nombre,
                "descripcion": paquete_turistico_turistico.tipo_paquete_id.descripcion,
                "estatus": paquete_turistico_turistico.tipo_paquete_id.estatus,
                "creado_en": paquete_turistico_turistico.tipo_paquete_id.creado_en,
                "modificado_en": paquete_turistico_turistico.tipo_paquete_id.modificado_en,
            },
            "duracion_dias": paquete_turistico_turistico.duracion_dias,
            "precio_base_bs": paquete_turistico_turistico.precio_base_bs,
            "capacidad_maxima_integrantes": paquete_turistico_turistico.capacidad_maxima_integrantes,
            "fecha_inico": paquete_turistico_turistico.fecha_inico,
            "fecha_fin": paquete_turistico_turistico.fecha_fin,
            "disponible": paquete_turistico_turistico.disponible,
            "estatus": paquete_turistico_turistico.estatus,
            "creado_en": paquete_turistico_turistico.creado_en,
            "modificado_en": paquete_turistico_turistico.modificado_en
        }
        return ResponseDTO.success(data=data)

    def get_paquetes_turisticos(self) -> ResponseDTO:
        paquetes_turisticos = self.repository.listar_todos()
        lista_data = [
            {
                "id": pt.id,
                "nombre": pt.nombre,
                "descripcion": pt.descripcion,
                "imagen_principal": pt.imagen_principal.url if pt.imagen_principal else None,
                "destino": {
                    "id": pt.destino_id.id,
                    "nombre": pt.destino_id.nombre,
                    "descripcion": pt.destino_id.descripcion,
                },
                "tipo_paquete": {
                    "id": pt.tipo_paquete_id.id,
                    "nombre": pt.tipo_paquete_id.nombre,
                    "descripcion": pt.tipo_paquete_id.descripcion,
                    "estatus": pt.tipo_paquete_id.estatus,
                    "creado_en": pt.tipo_paquete_id.creado_en,
                    "modificado_en": pt.tipo_paquete_id.modificado_en,
                },
                "duracion_dias": pt.duracion_dias,
                "precio_base_bs": pt.precio_base_bs,
                "capacidad_maxima_integrantes": pt.capacidad_maxima_integrantes,
                "fecha_inico": pt.fecha_inico,
                "fecha_fin": pt.fecha_fin,
                "disponible": pt.disponible,
                "estatus": pt.estatus,
                "creado_en": pt.creado_en,
                "modificado_en": pt.modificado_en
            }
            for pt in paquetes_turisticos
        ]
        return ResponseDTO.success(data=lista_data)

    def update_paquete_turistico(self, paquete_turistico_id: int, request_dto) -> ResponseDTO:
        try:
            # Primero verificamos existencia
            paquete_turistico_existente = self.repository.obtener_por_id(paquete_turistico_id)
            if not paquete_turistico_existente:
                return ResponseDTO.error("Paquete Turistico no encontrado para actualizar", "404")

            datos = request_dto.data
            archivo_imagen = datos.get('imagen_principal', None)

            paquete_turistico_actualizado = self.repository.actualizar_paquete_turistico(paquete_turistico_id, datos, archivo_imagen)
            return ResponseDTO.success(
                data={"id": paquete_turistico_actualizado.id},
                mensaje="Paquete Turistico actualizado correctamente"
            )
        except Exception as e:
            return ResponseDTO.error(str(e))

    def delete_paquete_turistico(self, paquete_turistico_id: int) -> ResponseDTO:
        exito = self.repository.eliminar_paquete_turistico(paquete_turistico_id)
        if exito:
            return ResponseDTO.success(mensaje="Paquete Turistico eliminado")
        return ResponseDTO.error("No se pudo eliminar el Paquete Turistico", "400")
