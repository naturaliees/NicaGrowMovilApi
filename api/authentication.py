from hmac import compare_digest
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class ApiKeyUser:
    is_authenticated = True
    is_anonymous = False


class ApiKeyAuthentication(BaseAuthentication):
    """Autenticación simple para aplicaciones móviles y clientes de reportes."""

    def authenticate(self, request):
        supplied = request.headers.get("X-Api-Key", "")
        if not supplied or not compare_digest(supplied, settings.API_KEY):
            raise AuthenticationFailed("X-Api-Key ausente o inválida.")
        return (ApiKeyUser(), None)

    def authenticate_header(self, request):
        return "ApiKey"
