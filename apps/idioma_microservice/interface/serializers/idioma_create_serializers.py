from rest_framework import serializers

class IdiomaCreateSerializer(serializers.Serializer):
    """
    Serializador para validar la creación de un nuevo idioma.
    JSON esperado: { "nombre_idioma": str }
    """
    
    # nombre_idioma: Obligatorio, debe ser string, no permite nulos ni vacíos.
    nombre_idioma = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=50,
        error_messages={
            'required': 'El campo nombre_idioma es obligatorio.',
            'blank': 'El nombre del idioma no puede estar vacío.',
            'invalid': 'El nombre del idioma debe ser una cadena de texto válida.',
            'max_length': 'El nombre del idioma no puede exceder los 50 caracteres.'
        }
    )

    def validate_nombre_idioma(self, value):
        """
        Limpia espacios y normaliza el texto (Primera letra en mayúscula).
        """
        return value.strip().capitalize()