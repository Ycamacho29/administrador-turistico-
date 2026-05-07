from rest_framework import serializers

class MonedaUpdateSerializer(serializers.Serializer):
    """
    Serializador para validar la actualización de una moneda.
    JSON esperado: { "nombre_moneda": str, "acronimo": str, "estatus": str }
    """
    
    # nombre_moneda: Obligatorio, string, máximo 50 caracteres.
    nombre_moneda = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=50,
        error_messages={
            'required': 'El nombre de la moneda es obligatorio.',
            'blank': 'El nombre de la moneda no puede estar vacío.',
        }
    )

    # acronimo: Obligatorio, string, longitud estándar ISO (3-5 caracteres).
    acronimo = serializers.CharField(
        required=True,
        allow_blank=False,
        min_length=3,
        max_length=5,
        error_messages={
            'required': 'El acrónimo es obligatorio.',
            'min_length': 'El acrónimo debe tener al menos 3 caracteres.',
            'max_length': 'El acrónimo no puede exceder los 5 caracteres.'
        }
    )

    # estatus: Obligatorio, string, longitud exacta de 1 carácter.
    estatus = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=1,
        min_length=1,
        error_messages={
            'required': 'El estatus es obligatorio.',
            'max_length': 'El estatus debe ser un único carácter (ej. A o I).',
        }
    )

    def validate_nombre_moneda(self, value):
        """Limpia espacios en blanco."""
        return value.strip()

    def validate_acronimo(self, value):
        """Normaliza el acrónimo a mayúsculas."""
        return value.strip().upper()

    def validate_estatus(self, value):
        """Normaliza el estatus y valida que sea una letra."""
        value = value.strip().upper()
        if not value.isalpha():
            raise serializers.ValidationError("El estatus debe ser una letra (A o I).")
        return value