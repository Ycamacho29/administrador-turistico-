from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


class EmailService:
    @staticmethod
    def enviar_confirmacion_viaje(email_cliente: str, datos_viaje: dict) -> bool:
        """
        Compila una plantilla HTML y envía el correo de confirmación al cliente.
        """
        try:
            asunto = f"¡Tu viaje a {datos_viaje['paquete_turistico']['destino']['nombre']} está confirmado! ✈️"

            # Renderizamos un archivo HTML pasándole las variables del viaje
            html_content = render_to_string(
                'emails/confirmacion_viaje.html', {'viaje': datos_viaje})

            # Texto plano de respaldo si el gestor de correos del cliente no soporta HTML
            text_content = strip_tags(html_content)

            correo = EmailMultiAlternatives(
                subject=asunto,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email_cliente]
            )
            correo.attach_alternative(html_content, "text/html")
            correo.send()
            return True
        except Exception as e:
            print(f"Error enviando correo: {str(e)}")
            return False
