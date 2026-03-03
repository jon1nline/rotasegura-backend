"""
Throttle classes para rate limiting da API.
Limita a quantidade de requisições por minuto para proteção contra abuso.
"""

from rest_framework.throttling import SimpleRateThrottle


class AnonRateThrottle(SimpleRateThrottle):
    """
    Throttle para usuários anônimos (não autenticados).
    10 requisições por minuto.
    """
    scope = 'anon'

    def get_cache_key(self, request, view):
        if request.user and request.user.is_authenticated:
            return None  # Usuários autenticados usam 'user' scope

        return self.cache_format % {
            'scope': self.scope,
            'ident': self.get_ident(request)
        }


class UserRateThrottle(SimpleRateThrottle):
    """
    Throttle para usuários autenticados.
    100 requisições por minuto.
    """
    scope = 'user'

    def get_cache_key(self, request, view):
        if request.user and request.user.is_authenticated:
            return self.cache_format % {
                'scope': self.scope,
                'ident': request.user.id
            }

        return None  # Usuários anônimos usam 'anon' scope


class AuthThrottle(SimpleRateThrottle):
    """
    Throttle específico para endpoints de autenticação (login/register).
    3 requisições por minuto.
    """
    scope = 'auth'

    def get_cache_key(self, request, view):
        return self.cache_format % {
            'scope': self.scope,
            'ident': self.get_ident(request)
        }


class CreateAnonThrottle(SimpleRateThrottle):
    """
    Throttle para criação de recursos (POST) por usuários anônimos.
    - Anônimos: 5/min
    """
    scope = 'create_anon'

    def get_cache_key(self, request, view):
        if request.user and request.user.is_authenticated:
            return None

        return self.cache_format % {
            'scope': self.scope,
            'ident': self.get_ident(request)
        }


class CreateUserThrottle(SimpleRateThrottle):
    """
    Throttle para criação de recursos (POST) por usuários autenticados.
    - Autenticados: 50/min
    """
    scope = 'create_auth'

    def get_cache_key(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return None

        return self.cache_format % {
            'scope': self.scope,
            'ident': request.user.id
        }


class ListAnonThrottle(SimpleRateThrottle):
    """
    Throttle para listagem (GET) por usuários anônimos.
    - Anônimos: 20/min
    """
    scope = 'list_anon'

    def get_cache_key(self, request, view):
        if request.user and request.user.is_authenticated:
            return None

        return self.cache_format % {
            'scope': self.scope,
            'ident': self.get_ident(request)
        }


class ListUserThrottle(SimpleRateThrottle):
    """
    Throttle para listagem (GET) por usuários autenticados.
    - Autenticados: 200/min
    """
    scope = 'list_auth'

    def get_cache_key(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return None

        return self.cache_format % {
            'scope': self.scope,
            'ident': request.user.id
        }
