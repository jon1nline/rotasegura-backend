from rest_framework.authentication import TokenAuthentication


class BearerTokenAuthentication(TokenAuthentication):
    """
    Autenticação via token usando o prefixo 'Bearer' em vez de 'Token'.
    Aceita: Authorization: Bearer <token>
    """
    keyword = 'Bearer'
