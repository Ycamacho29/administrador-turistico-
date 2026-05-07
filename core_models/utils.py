import secrets

def generar_codigo_pago():
    caracteres = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    return ''.join(secrets.choice(caracteres) for _ in range(8))