from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (CatalogView, DatabaseHealthView, ReportView, CiudadViewSet, ClienteViewSet, EstadoViewSet,
    MetodoEnvioViewSet, MetodoPagoViewSet, ProductoViewSet, TemporadaViewSet, TiempoViewSet, VendedorViewSet,
    BusquedaViewSet, IncidenteViewSet, TendenciaViewSet, ValoracionViewSet, VentaViewSet)

router = DefaultRouter()
router.register("ciudades", CiudadViewSet, basename="ciudad")
router.register("clientes", ClienteViewSet, basename="cliente")
router.register("estados", EstadoViewSet, basename="estado")
router.register("metodos-envio", MetodoEnvioViewSet, basename="metodo-envio")
router.register("metodos-pago", MetodoPagoViewSet, basename="metodo-pago")
router.register("productos", ProductoViewSet, basename="producto")
router.register("temporadas", TemporadaViewSet, basename="temporada")
router.register("tiempos", TiempoViewSet, basename="tiempo")
router.register("vendedores", VendedorViewSet, basename="vendedor")
router.register("busquedas", BusquedaViewSet, basename="busqueda")
router.register("incidentes", IncidenteViewSet, basename="incidente")
router.register("tendencias", TendenciaViewSet, basename="tendencia")
router.register("valoraciones", ValoracionViewSet, basename="valoracion")
router.register("ventas", VentaViewSet, basename="venta")

urlpatterns = [
    path("", CatalogView.as_view()),
    path("health/", DatabaseHealthView.as_view()),
    path("reportes/<str:report>/", ReportView.as_view()),
] + router.urls
