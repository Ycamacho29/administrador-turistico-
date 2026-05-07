from rest_framework import serializers

class PaisCreateSerializer(serializers.Serializer):
    """
    Serializador para validar la creación de un país.
    JSON esperado: { "nombre_pais": str }
    """
    
    # nombre_pais: Obligatorio, tipo string (CharField), no permite vacíos
    nombre_pais = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            'required': 'El campo nombre_pais es obligatorio.',
            'blank': 'El nombre del país no puede ser un texto vacío.',
            'invalid': 'El nombre del país debe ser una cadena de texto válida.'
        }
    )

    def validate_nombre_pais(self, value):
        """
        Validación adicional para limpiar espacios en blanco 
        y asegurar un formato consistente.
        """
        # Eliminamos espacios al inicio y final
        value = value.strip()
        
        if len(value) < 3:
            raise serializers.ValidationError("El nombre del país debe tener al menos 3 caracteres.")
            
        return value