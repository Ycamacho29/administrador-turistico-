from rest_framework import serializers
from decimal import Decimal

class PaqueteTuristicoUpdateSerializer(serializers.Serializer):
    """
    Serializador para validar la creación de paquetes turísticos.
    Incluye validaciones para fechas, montos decimales y relaciones.
    """
    
    # Campos de Texto
    nombre_paquete_turistico = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=150,
        error_messages={'required': 'El nombre del paquete es obligatorio.'}
    )
    
    descripcion = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        default=""
    )

    # IDs de Relaciones
    destino_id = serializers.IntegerField(required=True)
    tipo_paquete_id = serializers.IntegerField(required=True)

    # Campos Numéricos
    duracion_dias = serializers.IntegerField(
        required=True,
        min_value=1,
        error_messages={'min_value': 'La duración debe ser al menos de 1 día.'}
    )
    
    precio_base_bs = serializers.DecimalField(
        required=True,
        max_digits=15,
        decimal_places=2,
        min_value=Decimal('0.01')
    )
    
    capacidad_maxima_integrantes = serializers.IntegerField(
        required=True,
        min_value=1
    )

    # Fechas (Configuradas para el formato DD/MM/YYYY de tu JSON)
    fecha_inico = serializers.DateField(
        required=True,
        input_formats=['%d/%m/%Y'],
        error_messages={'invalid': 'Formato de fecha de inicio inválido. Use DD/MM/YYYY.'}
    )
    
    fecha_fin = serializers.DateField(
        required=True,
        input_formats=['%d/%m/%Y'],
        error_messages={'invalid': 'Formato de fecha de fin inválido. Use DD/MM/YYYY.'}
    )

    # Estados (Tipo String)
    disponible = serializers.CharField(
        required=True,
        max_length=1,
        min_length=1
    )
    
    estatus = serializers.CharField(
        required=True,
        max_length=1,
        min_length=1
    )

    imagen_principal = serializers.ImageField(
        required=False,
        allow_null=True,
        error_messages={
            'invalid': 'El archivo subido no es una imagen válida o está corrupto.'
        }
    )

    def validate_descripcion(self, value):
        """Garantiza que retorne un string vacío si no hay contenido."""
        return value.strip() if value else ""

    def validate_disponible(self, value):
        return value.strip().upper()

    def validate_estatus(self, value):
        return value.strip().upper()
    
    def validate_imagen_principal(self, value):
        """Validaciones personalizadas para el tamaño o peso del archivo."""
        if value:
            # Validar que la imagen no pese más de 2MB (2 * 1024 * 1024 bytes)
            max_size = 2 * 1024 * 1024
            if value.size > max_size:
                raise serializers.ValidationError(
                    "La imagen es muy pesada. El tamaño máximo permitido es de 2MB.")

            # Validar extensiones explícitas para restringir formatos específicos
            extension = value.name.split('.')[-1].lower()
            if extension not in ['jpg', 'jpeg', 'png', 'webp']:
                raise serializers.ValidationError(
                    "Formato de imagen no permitido. Usa JPG, JPEG, PNG o WEBP.")

        return value

    def validate(self, data):
        """
        Validación cruzada de fechas:
        Asegura que la fecha de fin no sea anterior a la de inicio.
        """
        if data['fecha_fin'] < data['fecha_inico']:
            raise serializers.ValidationError({
                "fecha_fin": "La fecha de finalización no puede ser anterior a la fecha de inicio."
            })
        return data