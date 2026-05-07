from apps.moneda_microservice.domain.entities.response import ResponseDTO

class MonedaUseCases:
    def __init__(self, repository):
        """
        Inyectamos el repositorio para que el caso de uso 
        no dependa de una base de datos específica.
        """
        self.repository = repository

    def create_moneda(self, request_dto) -> ResponseDTO:
        '''Ejecuta la lógica de negocio para el registro de una nueva moneda'''
        try:
            datos = request_dto.data

            nueva_moneda = self.repository.guardar_moneda(datos)

            return ResponseDTO.success(
                data={
                    "id": nueva_moneda.id,
                    "nombre": nueva_moneda.nombre,
                    "acronimo": nueva_moneda.acronimo
                },
                mensaje="Moneda creada exitosamente"
            )
        except Exception as e:
            return ResponseDTO.error(str(e))

    def get_moneda(self, moneda_id: int) -> ResponseDTO:
        moneda = self.repository.obtener_por_id(moneda_id)
        if not moneda:
            return ResponseDTO.error("Moneda no encontrada", "404")

        data = {
            "id": moneda.id,
            "nombre": moneda.nombre,
            "estatus": moneda.estatus,
            "acronimo": moneda.acronimo,
            "creado_en": moneda.creado_en,
            "modificado_en": moneda.modificado_en
        }
        return ResponseDTO.success(data=data)

    def get_monedas(self) -> ResponseDTO:
        monedas = self.repository.listar_todas()
        lista_data = [
            {
                "id": m.id,
                "nombre": m.nombre,
                "acronimo": m.acronimo,
                "estatus": m.estatus,
                "creado_en": m.creado_en,
                "modificado_en": m.modificado_en
            }
            for m in monedas
        ]
        return ResponseDTO.success(data=lista_data)

    def update_moneda(self, moneda_id: int, request_dto) -> ResponseDTO:
        try:
            # Primero verificamos existencia
            moneda_existente = self.repository.obtener_por_id(moneda_id)
            if not moneda_existente:
                return ResponseDTO.error("Moneda no encontrada para actualizar", "404")

            moneda_actualizada = self.repository.actualizar_moneda(moneda_id, request_dto.data)
            return ResponseDTO.success(
                data={"id": moneda_actualizada.id},
                mensaje="Moneda actualizada correctamente"
            )
        except Exception as e:
            return ResponseDTO.error(str(e))

    def delete_moneda(self, moneda_id: int) -> ResponseDTO:
        exito = self.repository.eliminar_moneda(moneda_id)
        if exito:
            return ResponseDTO.success(mensaje="Moneda eliminada")
        return ResponseDTO.error("No se pudo eliminar la moneda", "400")
