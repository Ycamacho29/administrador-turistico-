from apps.ciudad_microservice.domain.entities.response import ResponseDTO


class ReservaUseCases:
    def __init__(self, repository):
        """
        Inyectamos el repositorio para que el caso de uso 
        no dependa de una base de datos específica.
        """
        self.repository = repository

    def create_reserva(self, request_dto) -> ResponseDTO:
        '''Ejecuta la lógica de negocio para el registro de una nueva Reserva'''
        try:
            # Lógica de negocio
            datos = request_dto.data

            nueva_reserva = self.repository.guardar_reserva(datos)

            return ResponseDTO.success(
                data={
                    "id": nueva_reserva.id,
                    "codigo": nueva_reserva.codigo
                },
                mensaje="Reserva creada exitosamente"
            )

        except Exception as e:
            return ResponseDTO.error(str(e))

    def get_reserva(self, reserva_id: int) -> ResponseDTO:
        reserva = self.repository.obtener_por_id(reserva_id)
        if not reserva:
            return ResponseDTO.error("Reserva no encontrada", "404")

        # 1. Construimos la estructura base con los datos obligatorios
        reserva_json = {
            "id": reserva.id,
            "codigo": reserva.codigo,
            "paquete_turistico": {
                "id": reserva.paquete_id.id,
                "nombre": reserva.paquete_id.nombre,
                "descripcion": reserva.paquete_id.descripcion,
                "destino": {
                    "id": reserva.paquete_id.destino_id.id,
                    "nombre": reserva.paquete_id.destino_id.nombre,
                    "descripcion": reserva.paquete_id.destino_id.descripcion,
                },
                "tipo_paquete": {
                    "id": reserva.paquete_id.tipo_paquete_id.id,
                    "nombre": reserva.paquete_id.tipo_paquete_id.nombre,
                    "descripcion": reserva.paquete_id.tipo_paquete_id.descripcion,
                    "estatus": reserva.paquete_id.tipo_paquete_id.estatus,
                    "creado_en": reserva.paquete_id.tipo_paquete_id.creado_en,
                    "modificado_en": reserva.paquete_id.tipo_paquete_id.modificado_en,
                },
                "duracion_dias": reserva.paquete_id.duracion_dias,
                "precio_base_bs": reserva.paquete_id.precio_base_bs,
                "capacidad_maxima_integrantes": reserva.paquete_id.capacidad_maxima_integrantes,
                "fecha_inico": reserva.paquete_id.fecha_inico,
                "fecha_fin": reserva.paquete_id.fecha_fin,
                "disponible": reserva.paquete_id.disponible,
                "estatus": reserva.paquete_id.estatus,
            },
            "cliente": {
                "id": reserva.cliente_id.id,
                "primer_nombre": reserva.cliente_id.primer_nombre,
                "segundo_nombre": reserva.cliente_id.segundo_nombre,
                "primer_apellido": reserva.cliente_id.primer_apellido,
                "segundo_apellido": reserva.cliente_id.segundo_apellido,
                "telefono": reserva.cliente_id.telefono,
                "cedula": reserva.cliente_id.cedula,
                "creado_en": reserva.cliente_id.creado_en,
                "modificado_en": reserva.cliente_id.modificado_en
            },
            "cantidad_personas": reserva.cantidad_personas,
            "estatus": {
                "id": reserva.estatus_id.id,
                "nombre": reserva.estatus_id.nombre,
                "descripcion": reserva.estatus_id.descripcion,
                "estatus": reserva.estatus_id.estatus,
            },
            "creado_en": reserva.creado_en,
            "modificado_en": reserva.modificado_en
        }

        # 2. Validamos si existe la relación de pago antes de agregar la llave
        if reserva.pago_id is not None:
            reserva_json["pago"] = {
                "id": reserva.pago_id.id,
                "codigo_referencia": reserva.pago_id.codigo_referencia,
                "metodo_pago": {
                    "id": reserva.pago_id.metodo_pago_id.id,
                    "nombre": reserva.pago_id.metodo_pago_id.nombre,
                    "estatus": reserva.pago_id.metodo_pago_id.estatus,
                },
                "estatus_pago": {
                    "id": reserva.pago_id.estatus_pago_id.id,
                    "nombre": reserva.pago_id.estatus_pago_id.nombre,
                    "descripcion": reserva.pago_id.estatus_pago_id.descripcion,
                    "estatus": reserva.pago_id.estatus_pago_id.estatus,
                },
                "moneda": {
                    "id": reserva.pago_id.moneda_id.id,
                    "nombre": reserva.pago_id.moneda_id.nombre,
                    "acronimo": reserva.pago_id.moneda_id.acronimo,
                    "estatus": reserva.pago_id.moneda_id.estatus
                },
                "monto_bs": reserva.pago_id.monto_bs,
                "monto_otra_moneda": reserva.pago_id.monto_otra_moneda,
                "taza_bs": reserva.pago_id.taza_bs,
            }

        return ResponseDTO.success(data=reserva_json)

    @staticmethod
    def get_reserva_x_id_pago(pago_id: int) -> ResponseDTO:

        from apps.reserva_microservice.infrastructure.repositories import ReservaRepository
        repository = ReservaRepository()

        reserva = repository.obtener_por_id_pago(pago_id)
        if not reserva:
            return ResponseDTO.error("Reserva no encontrada", "404")

        # 1. Construimos la estructura base con los datos obligatorios
        reserva_json = {
            "id": reserva.id,
            "codigo": reserva.codigo,
            "paquete_turistico": {
                "id": reserva.paquete_id.id,
                "nombre": reserva.paquete_id.nombre,
                "descripcion": reserva.paquete_id.descripcion,
                "destino": {
                    "id": reserva.paquete_id.destino_id.id,
                    "nombre": reserva.paquete_id.destino_id.nombre,
                    "descripcion": reserva.paquete_id.destino_id.descripcion,
                },
                "tipo_paquete": {
                    "id": reserva.paquete_id.tipo_paquete_id.id,
                    "nombre": reserva.paquete_id.tipo_paquete_id.nombre,
                    "descripcion": reserva.paquete_id.tipo_paquete_id.descripcion,
                    "estatus": reserva.paquete_id.tipo_paquete_id.estatus,
                    "creado_en": reserva.paquete_id.tipo_paquete_id.creado_en,
                    "modificado_en": reserva.paquete_id.tipo_paquete_id.modificado_en,
                },
                "duracion_dias": reserva.paquete_id.duracion_dias,
                "precio_base_bs": reserva.paquete_id.precio_base_bs,
                "capacidad_maxima_integrantes": reserva.paquete_id.capacidad_maxima_integrantes,
                "fecha_inico": reserva.paquete_id.fecha_inico,
                "fecha_fin": reserva.paquete_id.fecha_fin,
                "disponible": reserva.paquete_id.disponible,
                "estatus": reserva.paquete_id.estatus,
            },
            "cliente": {
                "id": reserva.cliente_id.id,
                "primer_nombre": reserva.cliente_id.primer_nombre,
                "segundo_nombre": reserva.cliente_id.segundo_nombre,
                "primer_apellido": reserva.cliente_id.primer_apellido,
                "segundo_apellido": reserva.cliente_id.segundo_apellido,
                "telefono": reserva.cliente_id.telefono,
                "cedula": reserva.cliente_id.cedula,
                "creado_en": reserva.cliente_id.creado_en,
                "modificado_en": reserva.cliente_id.modificado_en
            },
            "cantidad_personas": reserva.cantidad_personas,
            "estatus": {
                "id": reserva.estatus_id.id,
                "nombre": reserva.estatus_id.nombre,
                "descripcion": reserva.estatus_id.descripcion,
                "estatus": reserva.estatus_id.estatus,
            },
            "creado_en": reserva.creado_en,
            "modificado_en": reserva.modificado_en
        }

        # 2. Validamos si existe la relación de pago antes de agregar la llave
        if reserva.pago_id is not None:
            reserva_json["pago"] = {
                "id": reserva.pago_id.id,
                "codigo_referencia": reserva.pago_id.codigo_referencia,
                "metodo_pago": {
                    "id": reserva.pago_id.metodo_pago_id.id,
                    "nombre": reserva.pago_id.metodo_pago_id.nombre,
                    "estatus": reserva.pago_id.metodo_pago_id.estatus,
                },
                "estatus_pago": {
                    "id": reserva.pago_id.estatus_pago_id.id,
                    "nombre": reserva.pago_id.estatus_pago_id.nombre,
                    "descripcion": reserva.pago_id.estatus_pago_id.descripcion,
                    "estatus": reserva.pago_id.estatus_pago_id.estatus,
                },
                "moneda": {
                    "id": reserva.pago_id.moneda_id.id,
                    "nombre": reserva.pago_id.moneda_id.nombre,
                    "acronimo": reserva.pago_id.moneda_id.acronimo,
                    "estatus": reserva.pago_id.moneda_id.estatus
                },
                "monto_bs": reserva.pago_id.monto_bs,
                "monto_otra_moneda": reserva.pago_id.monto_otra_moneda,
                "taza_bs": reserva.pago_id.taza_bs,
            }

        return ResponseDTO.success(data=reserva_json)


    def get_reservas(self) -> ResponseDTO:
        reservas = self.repository.listar_todas()
        lista_data = []

        for r in reservas:
            # 1. Estructura base con campos que SIEMPRE van a existir
            reserva_json = {
                "id": r.id,
                "codigo": r.codigo,
                "paquete_turistico": {
                    "id": r.paquete_id.id,
                    "nombre": r.paquete_id.nombre,
                    "descripcion": r.paquete_id.descripcion,
                    "destino": {
                        "id": r.paquete_id.destino_id.id,
                        "nombre": r.paquete_id.destino_id.nombre,
                        "descripcion": r.paquete_id.destino_id.descripcion,
                    },
                    "tipo_paquete": {
                        "id": r.paquete_id.tipo_paquete_id.id,
                        "nombre": r.paquete_id.tipo_paquete_id.nombre,
                        "descripcion": r.paquete_id.tipo_paquete_id.descripcion,
                        "estatus": r.paquete_id.tipo_paquete_id.estatus,
                        "creado_en": r.paquete_id.tipo_paquete_id.creado_en,
                        "modificado_en": r.paquete_id.tipo_paquete_id.modificado_en,
                    },
                    "duracion_dias": r.paquete_id.duracion_dias,
                    "precio_base_bs": r.paquete_id.precio_base_bs,
                    "capacidad_maxima_integrantes": r.paquete_id.capacidad_maxima_integrantes,
                    "fecha_inico": r.paquete_id.fecha_inico,
                    "fecha_fin": r.paquete_id.fecha_fin,
                    "disponible": r.paquete_id.disponible,
                    "estatus": r.paquete_id.estatus,
                },
                "cliente": {
                    "id": r.cliente_id.id,
                    "primer_nombre": r.cliente_id.primer_nombre,
                    "segundo_nombre": r.cliente_id.segundo_nombre,
                    "primer_apellido": r.cliente_id.primer_apellido,
                    "segundo_apellido": r.cliente_id.segundo_apellido,
                    "telefono": r.cliente_id.telefono,
                    "cedula": r.cliente_id.cedula,
                    "creado_en": r.cliente_id.creado_en,
                    "modificado_en": r.cliente_id.modificado_en
                },
                "cantidad_personas": r.cantidad_personas,
                "estatus": {
                    "id": r.estatus_id.id,
                    "nombre": r.estatus_id.nombre,
                    "descripcion": r.estatus_id.descripcion,
                    "estatus": r.estatus_id.estatus,
                },
                "creado_en": r.creado_en,
                "modificado_en": r.modificado_en
            }

            # 2. Evaluación condicional para la llave "pago"
            # Si r.pago_id existe (no es None), inyectamos la estructura completa
            if r.pago_id is not None:
                reserva_json["pago"] = {
                    "id": r.pago_id.id,
                    "codigo_referencia": r.pago_id.codigo_referencia,
                    "metodo_pago": {
                        "id": r.pago_id.metodo_pago_id.id,
                        "nombre": r.pago_id.metodo_pago_id.nombre,
                        "estatus": r.pago_id.metodo_pago_id.estatus,
                    },
                    "estatus_pago": {
                        "id": r.pago_id.estatus_pago_id.id,
                        "nombre": r.pago_id.estatus_pago_id.nombre,
                        "descripcion": r.pago_id.estatus_pago_id.descripcion,
                        "estatus": r.pago_id.estatus_pago_id.estatus,
                    },
                    "moneda": {
                        "id": r.pago_id.moneda_id.id,
                        "nombre": r.pago_id.moneda_id.nombre,
                        "acronimo": r.pago_id.moneda_id.acronimo,
                        "estatus": r.pago_id.moneda_id.estatus
                    },
                    "monto_bs": r.pago_id.monto_bs,
                    "monto_otra_moneda": r.pago_id.monto_otra_moneda,
                    "taza_bs": r.pago_id.taza_bs,
                }

            # 3. Guardamos el diccionario procesado en nuestra lista de salida
            lista_data.append(reserva_json)

        return ResponseDTO.success(data=lista_data)

    def update_reserva(self, reserva_id: int, request_dto) -> ResponseDTO:
        try:
            # Primero verificamos existencia
            reserva_existente = self.repository.obtener_por_id(reserva_id)
            if not reserva_existente:
                return ResponseDTO.error("Reserva no encontrada para actualizar", "404")

            reserva_actualizada = self.repository.actualizar_reserva(reserva_id, request_dto.data)
            return ResponseDTO.success(
                data={"id": reserva_actualizada.id},
                mensaje="Reserva actualizada correctamente"
            )
        except Exception as e:
            return ResponseDTO.error(str(e))

    def delete_reserva(self, reserva_id: int) -> ResponseDTO:
        exito = self.repository.eliminar_reserva(reserva_id)
        if exito:
            return ResponseDTO.success(mensaje="Reserva eliminada")
        return ResponseDTO.error("No se pudo eliminar la Reserva", "400")
