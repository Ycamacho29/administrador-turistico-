from rest_framework import serializers


class ReservaUpdateSerializer(serializers.Serializer):
    """
    Serializador para validar el cambio de estatus de una reserva.
    pago_id es opcional y convierte el string vacío "" a None de manera segura.
    """

    # pago_id: Opcional. Permite enteros, null o strings vacíos.
    pago_id = serializers.IntegerField(
        required=False,
        allow_null=True,
        default=None
    )

    # estatus_id: Obligatorio y debe ser un número entero.
    estatus_id = serializers.IntegerField(
        required=True,
        error_messages={'required': 'El ID del estatus es obligatorio.'}
    )

    def __init__(self, *args, **kwargs):
        """
        Intercepta los datos antes de la validación de DRF.
        Si 'pago_id' viene como una cadena vacía "", lo normaliza a None.
        """
        input_data = kwargs.get('data', None)
        if input_data and 'pago_id' in input_data:
            if input_data['pago_id'] == "":
                input_data['pago_id'] = None
        super().__init__(*args, **kwargs)

    def validate_estatus_id(self, value):
        """Asegura que el ID de estatus sea un identificador válido mayor a cero."""
        if value <= 0:
            raise serializers.ValidationError(
                "El ID del estatus debe ser un número entero positivo.")
        return value
