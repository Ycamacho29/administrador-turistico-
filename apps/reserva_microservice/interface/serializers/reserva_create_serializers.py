from rest_framework import serializers

class ReservaCreateSerializer(serializers.Serializer):
    """
    Serializador para validar la creación de una reserva.
    pago_id es opcional y maneja la conversión de vacío a None (NULL).
    """
    
    # pago_id: Opcional. Acepta números enteros, strings vacíos o null.
    pago_id = serializers.IntegerField(
        required=False,
        allow_null=True,
        default=None
    )

    # Campos obligatorios de tipo entero
    paquete_id = serializers.IntegerField(
        required=True,
        error_messages={'required': 'El ID del paquete es obligatorio.'}
    )
    
    cliente_id = serializers.IntegerField(
        required=True,
        error_messages={'required': 'El ID del cliente es obligatorio.'}
    )
    
    cantidad_personas = serializers.IntegerField(
        required=True,
        min_value=1,
        error_messages={
            'required': 'La cantidad de personas es obligatoria.',
            'min_value': 'La cantidad de personas debe ser al menos 1.'
        }
    )
    
    estatus_id = serializers.IntegerField(
        required=True,
        error_messages={'required': 'El ID del estatus es obligatorio.'}
    )

    def __init__(self, *args, **kwargs):
        """
        Interceptamos los datos de entrada para limpiar el JSON 
        si 'pago_id' viene como un string vacío ("").
        """
        input_data = kwargs.get('data', None)
        if input_data and 'pago_id' in input_data:
            if input_data['pago_id'] == "":
                input_data['pago_id'] = None
        super().__init__(*args, **kwargs)

    def validate(self, data):
        """Validación general de integridad para los IDs obligatorios."""
        for campo in ['paquete_id', 'cliente_id', 'estatus_id']:
            if data.get(campo, 0) <= 0:
                raise serializers.ValidationError({
                    campo: "El ID debe ser un número entero positivo."
                })
        return data