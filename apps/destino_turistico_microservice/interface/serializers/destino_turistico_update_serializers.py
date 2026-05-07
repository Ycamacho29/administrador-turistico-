from rest_framework import serializers

class DestinoTuristicoUpdateSerializer(serializers.Serializer):
    """
    Serializador para validar la actualización de un destino turístico.
    Todos los campos son obligatorios excepto 'descripcion'.
    """
    
    # nombre_destino_turistico: Obligatorio, string.
    nombre_destino_turistico = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=150,
        error_messages={'required': 'El nombre del destino es obligatorio.'}
    )

    # descripcion: Opcional. Si no viene o es nula, retorna "".
    descripcion = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        default=""
    )

    # IDs de Relaciones: Obligatorios y enteros.
    pais_id = serializers.IntegerField(required=True)
    ciudad_id = serializers.IntegerField(required=True)
    idioma_id = serializers.IntegerField(required=True)
    moneda_id = serializers.IntegerField(required=True)

    # estatus: Obligatorio, string de 1 carácter (A o I).
    estatus = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=1,
        min_length=1,
        error_messages={
            'required': 'El estatus es obligatorio.',
            'max_length': 'El estatus debe ser un único carácter.'
        }
    )

    def validate_nombre_destino_turistico(self, value):
        """Limpia espacios en blanco."""
        return value.strip()

    def validate_descripcion(self, value):
        """Normaliza la descripción para que nunca sea None."""
        return value.strip() if value else ""

    def validate_estatus(self, value):
        """Normaliza el estatus a mayúscula."""
        return value.strip().upper()

    def validate(self, data):
        """Validación de integridad para los IDs."""
        for campo in ['pais_id', 'ciudad_id', 'idioma_id', 'moneda_id']:
            if data.get(campo, 0) <= 0:
                raise serializers.ValidationError({
                    campo: "El ID proporcionado debe ser un número entero positivo."
                })
        return data