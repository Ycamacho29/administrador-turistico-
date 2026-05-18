from rest_framework import serializers

class PaqueteServicioCreateSerializer(serializers.Serializer):
    """
    Serializador para validar la asignación de un servicio a un paquete turístico.
    Ambos campos son obligatorios y deben ser números enteros positivos.
    """

    paquete_turistico_id = serializers.IntegerField(
        required=True,
        min_value=1,
        error_messages={
            'required': 'El ID del paquete turístico es obligatorio.',
            'invalid': 'El ID del paquete turístico debe ser un número entero válido.',
            'min_value': 'El ID del paquete turístico debe ser un número entero positivo.'
        }
    )

    # Manteniendo el nombre exacto de tu atributo 'servico_id'
    servico_id = serializers.IntegerField(
        required=True,
        min_value=1,
        error_messages={
            'required': 'El ID del servicio es obligatorio.',
            'invalid': 'El ID del servicio debe ser un número entero válido.',
            'min_value': 'El ID del servicio debe ser un número entero positivo.'
        }
    )

    def validate(self, data):
        """
        Validaciones de integridad adicionales si se requieren en el futuro.
        Por los momentos, asegura el retorno limpio de los datos validados.
        """
        return data