from rest_framework import serializers

class MetodoPagoCreateSerializer(serializers.Serializer):
    """
    Serializador para validar la creación de un método de pago.
    JSON esperado: { "nombre_metodo_pago": str }
    """
    
    # nombre_metodo_pago: Obligatorio, string, máximo 50 caracteres.
    nombre_metodo_pago = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=50,
        error_messages={
            'required': 'El nombre del método de pago es obligatorio.',
            'blank': 'El nombre del método de pago no puede estar vacío.',
            'invalid': 'El nombre del método de pago debe ser una cadena de texto válida.',
            'max_length': 'El nombre del método de pago no puede exceder los 50 caracteres.'
        }
    )

    def validate_nombre_metodo_pago(self, value):
        """
        Limpia espacios y normaliza el texto (Primera letra en mayúscula).
        """
        return value.strip().title()