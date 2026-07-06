import pprint
from apps.pago_microservice.domain.entities.response import ResponseDTO
from apps.reserva_microservice.application.use_cases import ReservaUseCases
from apps.core.services.email_service import EmailService


class PagoUseCases:
    def __init__(self, repository):
        """
        Inyectamos el repositorio para que el caso de uso 
        no dependa de una base de datos específica.
        """
        self.repository = repository

    def create_pago(self, request_dto) -> ResponseDTO:
        '''Ejecuta la lógica de negocio para el registro de un nuevo pago'''
        try:
            # Lógica de negocio
            datos = request_dto.data

            archivo_imagen = datos.get('comprobante', None)

            nuevo_pago = self.repository.guardar_pago(datos, archivo_imagen)

            return ResponseDTO.success(
                data={
                    "id": nuevo_pago.id,
                    "codigo_referencia": nuevo_pago.codigo_referencia,
                    "monto_bs": nuevo_pago.monto_bs
                },
                mensaje="Pago creado exitosamente"
            )
        except Exception as e:
            return ResponseDTO.error(str(e))

    def get_pago(self, pago_id: int) -> ResponseDTO:
        pago = self.repository.obtener_por_id(pago_id)
        if not pago:
            return ResponseDTO.error("Pago no encontrado", "404")

        # Construimos la URL pública de la imagen de forma segura si el registro la tiene
        url_imagen = pago.comprobante.url if pago.comprobante else None

        data = {
            "id": pago.id,
            "codigo_referencia": pago.codigo_referencia,
            "comprobante": url_imagen,
            "metodo_pago": {
                "id": pago.metodo_pago_id.id,
                "nombre": pago.metodo_pago_id.nombre,
                "estatus": pago.metodo_pago_id.estatus,
                "creado_en": pago.metodo_pago_id.creado_en,
                "modificado_en": pago.metodo_pago_id.modificado_en
            },
            "estatus_pago": {
                "id": pago.estatus_pago_id.id,
                "nombre": pago.estatus_pago_id.nombre,
                "descripcion": pago.estatus_pago_id.descripcion,
                "estatus": pago.estatus_pago_id.estatus,
                "creado_en": pago.estatus_pago_id.creado_en,
                "modificado_en": pago.estatus_pago_id.modificado_en
            },
            "moneda": {
                "id": pago.moneda_id.id,
                "nombre": pago.moneda_id.nombre,
                "acronimo": pago.moneda_id.acronimo,
                "estatus": pago.moneda_id.estatus,
                "creado_en": pago.moneda_id.creado_en,
                "modificado_en": pago.moneda_id.modificado_en
            },
            "monto_bs": pago.monto_bs,
            "monto_otra_moneda": pago.monto_otra_moneda,
            "taza_bs": pago.taza_bs,
            "creado_en": pago.creado_en,
            "modificado_en": pago.modificado_en
        }
        return ResponseDTO.success(data=data)

    def get_pagos(self) -> ResponseDTO:
        pagos = self.repository.listar_todos()
        lista_data = [
            {
                "id": p.id,
                "codigo_referencia": p.codigo_referencia,
                "comprobante": p.comprobante.url if p.comprobante else None,
                "metodo_pago": {
                    "id": p.metodo_pago_id.id,
                    "nombre": p.metodo_pago_id.nombre,
                    "estatus": p.metodo_pago_id.estatus,
                    "creado_en": p.metodo_pago_id.creado_en,
                    "modificado_en": p.metodo_pago_id.modificado_en
                },
                "estatus_pago": {
                    "id": p.estatus_pago_id.id,
                    "nombre": p.estatus_pago_id.nombre,
                    "descripcion": p.estatus_pago_id.descripcion,
                    "estatus": p.estatus_pago_id.estatus,
                    "creado_en": p.estatus_pago_id.creado_en,
                    "modificado_en": p.estatus_pago_id.modificado_en
                },
                "moneda": {
                    "id": p.moneda_id.id,
                    "nombre": p.moneda_id.nombre,
                    "acronimo": p.moneda_id.acronimo,
                    "estatus": p.moneda_id.estatus,
                    "creado_en": p.moneda_id.creado_en,
                    "modificado_en": p.moneda_id.modificado_en
                },
                "monto_bs": p.monto_bs,
                "monto_otra_moneda": p.monto_otra_moneda,
                "taza_bs": p.taza_bs,
                "creado_en": p.creado_en,
                "modificado_en": p.modificado_en
            }
            for p in pagos
        ]
        return ResponseDTO.success(data=lista_data)

    def update_pago(self, pago_id: int, request_dto) -> ResponseDTO:
        try:
            # Primero verificamos existencia
            pago_existente = self.repository.obtener_por_id(pago_id)
            if not pago_existente:
                return ResponseDTO.error("Pago no encontrado para actualizar", "404")

            datos = request_dto.data
            archivo_imagen = datos.get('comprobante', None)

            pago_actualizado = self.repository.actualizar_pago(
                pago_id, datos, archivo_imagen)

            response_reserva = ReservaUseCases.get_reserva_x_id_pago(pago_id)

            datos_viaje = response_reserva.data

            correo_cliente = request_dto.metadata.usuario

            EmailService.enviar_confirmacion_viaje(
                email_cliente=correo_cliente, datos_viaje=datos_viaje)

            return ResponseDTO.success(
                data={"id": pago_actualizado.id},
                mensaje="Pago actualizado correctamente"
            )
        except Exception as e:
            return ResponseDTO.error(str(e))

    # def delete_pago(self, pago_id: int) -> ResponseDTO:
    #     exito = self.repository.eliminar_pago(pago_id)
    #     if exito:
    #         return ResponseDTO.success(mensaje="Pago eliminado")
    #     return ResponseDTO.error("No se pudo eliminar el pago", "400")
