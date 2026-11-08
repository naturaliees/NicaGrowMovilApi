from django.urls import include, path
from api.views import public_health

urlpatterns = [
    path("healthz/", public_health, name="healthz"),
    path("api/", include("api.urls")),
]
