from rest_framework import serializers

class IdiomaUpdateSerializer(serializers.Serializer):
    """
    Serializador para validar la actualización de un idioma.
    JSON esperado: { "nombre_idioma": str, "estatus": str }
    """
    
    # nombre_idioma: Obligatorio, string, máximo 50 caracteres.
    nombre_idioma = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=50,
        error_messages={
            'required': 'El nombre del idioma es obligatorio.',
            'blank': 'El nombre del idioma no puede estar vacío.',
            'invalid': 'El nombre del idioma debe ser una cadena de texto válida.'
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
            'blank': 'El estatus no puede estar vacío.',
            'max_length': 'El estatus debe ser un único carácter (ej. A o I).',
            'min_length': 'El estatus debe tener al menos un carácter.'
        }
    )

    def validate_nombre_idioma(self, value):
        """Limpia espacios en blanco innecesarios."""
        return value.strip()

    def validate_estatus(self, value):
        """Normaliza el estatus a mayúsculas y valida que sea una letra."""
        value = value.strip().upper()
        if not value.isalpha():
            raise serializers.ValidationError("El estatus debe ser una letra.")
        return value