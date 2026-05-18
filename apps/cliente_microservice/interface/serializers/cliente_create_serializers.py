from rest_framework import serializers


class ClienteCreateSerializer(serializers.Serializer):
    """
    Serializador para validar datos personales de una persona.
    Campos obligatorios: primer_nombre, primer_apellido, telefono, cedula.
    Campos opcionales: segundo_nombre, segundo_apellido.
    """

    # primer_nombre: Obligatorio, no puede estar en blanco.
    primer_nombre = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=50,
        error_messages={
            'required': 'El primer nombre es obligatorio.',
            'blank': 'El primer nombre no puede estar vacío.'
        }
    )

    # segundo_nombre: Opcional, permite blanco y nulo.
    segundo_nombre = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        default=""
    )

    # primer_apellido: Obligatorio.
    primer_apellido = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=50,
        error_messages={
            'required': 'El primer apellido es obligatorio.',
            'blank': 'El primer apellido no puede estar vacío.'
        }
    )

    # segundo_apellido: Opcional.
    segundo_apellido = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        default=""
    )

    # telefono: Obligatorio, string.
    telefono = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=12,
        error_messages={
            'required': 'El número de teléfono es obligatorio.',
            'blank': 'El teléfono no puede estar vacío.'
        }
    )

    # cedula: Obligatorio, string.
    cedula = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=10,
        error_messages={
            'required': 'La cédula es obligatoria.',
            'blank': 'La cédula no puede estar vacía.'
        }
    )

    def validate_telefono(self, value):
        """Limpia espacios o caracteres extraños en el teléfono."""
        print("".join(filter(str.isdigit, value)))
        valor = "".join(filter(str.isdigit, value))
        print(len(valor))
        return "".join(filter(str.isdigit, value))

    def validate_cedula(self, value):
        """Normaliza la cédula quitando puntos o guiones."""
        print(value.replace(".", "").replace("-", "").strip())
        valor = value.replace(".", "").replace("-", "").strip()
        print(len(valor))
        return value.replace(".", "").replace("-", "").strip()

    def validate(self, data):
        """Limpieza general de strings para evitar espacios innecesarios."""
        for campo in data:
            if isinstance(data[campo], str):
                data[campo] = data[campo].strip()
        print(data)
        return data
