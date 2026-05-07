from rest_framework import serializers

class MonedaCreateSerializer(serializers.Serializer):
    """
    Serializador para validar la creación de una moneda.
    JSON esperado: { "nombre_moneda": str, "acronimo": str }
    """
    
    # nombre_moneda: Obligatorio, string, máximo 50 caracteres.
    nombre_moneda = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=50,
        error_messages={
            'required': 'El nombre de la moneda es obligatorio.',
            'blank': 'El nombre de la moneda no puede estar vacío.',
            'invalid': 'El nombre de la moneda debe ser una cadena de texto.'
        }
    )

    # acronimo: Obligatorio, string de 3 caracteres (ISO 4217).
    acronimo = serializers.CharField(
        required=True,
        allow_blank=False,
        min_length=3,
        max_length=5, # Permitimos hasta 5 por si se usa formatos extendidos
        error_messages={
            'required': 'El acrónimo es obligatorio.',
            'blank': 'El acrónimo no puede estar vacío.',
            'min_length': 'El acrónimo debe tener al menos 3 caracteres.',
            'max_length': 'El acrónimo no puede exceder los 5 caracteres.'
        }
    )

    def validate_nombre_moneda(self, value):
        """Limpia y capitaliza el nombre de la moneda."""
        return value.strip().capitalize()

    def validate_acronimo(self, value):
        """Asegura que el acrónimo esté siempre en mayúsculas."""
        return value.strip().upper()