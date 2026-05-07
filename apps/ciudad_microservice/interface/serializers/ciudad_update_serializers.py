from rest_framework import serializers

class CiudadUpdateSerializer(serializers.Serializer):
    """
    Serializador para validar el JSON de entrada para actulizar una ciudad.
    """
    # nombre_ciudad: Obligatorio, string.
    nombre_ciudad = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={'required': 'El nombre de la ciudad es obligatorio.'}
    )

    # estatus: Obligatorio, exactamente 1 caracter, solo letras.
    estatus = serializers.CharField(
        required=True,
        min_length=1,
        max_length=1,
        error_messages={
            'required': 'El estatus es obligatorio.',
            'max_length': 'El estatus debe ser una única letra.',
            'min_length': 'El estatus no puede estar vacío.'
        }
    )

    # pais_id: Obligatorio, debe ser un número entero.
    pais_id = serializers.IntegerField(
        required=True,
        error_messages={
            'required': 'El ID del país es obligatorio.',
            'invalid': 'El pais_id debe ser un número entero válido.'
        }
    )

    def validate_estatus(self, value):
        """Valida que el estatus sea una letra y no un número o símbolo."""
        if not value.isalpha():
            raise serializers.ValidationError("El estatus debe ser una letra (A-Z).")
        return value.upper() # Lo normalizamos a mayúscula de una vez