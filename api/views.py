from django.db import connection
from django.db.models import CharField, TextField
from django.http import JsonResponse
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models
from .serializers import WarehouseSerializer


def public_health(request):
    return JsonResponse({"estado": "ok", "servicio": "NicaGrow API"})


class ReadOnlyWarehouseViewSet(viewsets.ReadOnlyModelViewSet):
    """Lectura paginada, filtros exactos y búsqueda de texto para una tabla DW."""
    serializer_class = WarehouseSerializer
    http_method_names = ["get", "head", "options"]

    def get_queryset(self):
        qs = self.queryset.all()
        fields = {field.name: field for field in self.queryset.model._meta.fields}
        for name, value in self.request.query_params.items():
            if name in {"pagina", "tamano", "orden", "buscar"}:
                continue
            if name not in fields:
                raise ValidationError({name: "Filtro no válido para este recurso."})
            try:
                qs = qs.filter(**{name: fields[name].to_python(value)})
            except (TypeError, ValueError):
                raise ValidationError({name: "Valor de filtro no válido."})
        term = self.request.query_params.get("buscar")
        if term:
            text_fields = [f.name for f in fields.values() if isinstance(f, (CharField, TextField))]
            from django.db.models import Q
            query = Q()
            for field in text_fields:
                query |= Q(**{f"{field}__icontains": term})
            qs = qs.filter(query)
        order = self.request.query_params.get("orden")
        if order:
            column = order.lstrip("-")
            if column not in fields:
                raise ValidationError({"orden": "Campo de orden no válido."})
            qs = qs.order_by(order)
        return qs


def resource_viewset(model):
    return type(f"{model.__name__}ViewSet", (ReadOnlyWarehouseViewSet,), {
        "queryset": model.objects.all(),
        "serializer_class": type(f"{model.__name__}Serializer", (WarehouseSerializer,), {"Meta": type("Meta", (), {"model": model, "fields": "__all__"})}),
    })


CiudadViewSet = resource_viewset(models.DimCiudad)
ClienteViewSet = resource_viewset(models.DimCliente)
EstadoViewSet = resource_viewset(models.DimEstado)
MetodoEnvioViewSet = resource_viewset(models.DimMetodoEnvio)
MetodoPagoViewSet = resource_viewset(models.DimMetodoPago)
ProductoViewSet = resource_viewset(models.DimProducto)
TemporadaViewSet = resource_viewset(models.DimTemporada)
TiempoViewSet = resource_viewset(models.DimTiempo)
VendedorViewSet = resource_viewset(models.DimVendedor)
BusquedaViewSet = resource_viewset(models.FactBusquedas)
IncidenteViewSet = resource_viewset(models.FactIncidentes)
TendenciaViewSet = resource_viewset(models.FactTendenciaTemporada)
ValoracionViewSet = resource_viewset(models.FactValoraciones)
VentaViewSet = resource_viewset(models.FactVentas)


class CatalogView(APIView):
    def get(self, request):
        return Response({"nombre": "NicaGrow Data Warehouse API", "version": "1.0", "documentacion": "/api/", "salud": "/api/health/", "recursos": [
            "ciudades", "clientes", "estados", "metodos-envio", "metodos-pago", "productos", "temporadas", "tiempos", "vendedores", "busquedas", "incidentes", "tendencias", "valoraciones", "ventas"
        ]})


class DatabaseHealthView(APIView):
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        return Response({"estado": "ok", "base_de_datos": "conectada"})


class ReportView(APIView):
    QUERIES = {
        "resumen-ventas": "SELECT COUNT(*) AS total_ventas, COALESCE(SUM(ImporteVenta),0) AS importe_total, COALESCE(SUM(Cantidad),0) AS unidades FROM [dw].[Fact_Ventas]",
        "ventas-mensuales": "SELECT t.Anio, t.Mes, COALESCE(SUM(v.ImporteVenta),0) AS importe_total, COALESCE(SUM(v.Cantidad),0) AS unidades FROM [dw].[Fact_Ventas] v JOIN [dw].[Dim_Tiempo] t ON v.TiempoKey=t.TiempoKey GROUP BY t.Anio,t.Mes ORDER BY t.Anio,t.Mes",
        "top-productos": "SELECT TOP (10) p.NombreProducto, p.Categoria, COALESCE(SUM(v.Cantidad),0) AS unidades, COALESCE(SUM(v.ImporteVenta),0) AS importe_total FROM [dw].[Fact_Ventas] v JOIN [dw].[Dim_Producto] p ON v.ProductoKey=p.ProductoKey GROUP BY p.NombreProducto,p.Categoria ORDER BY importe_total DESC",
        "ventas-ciudad": "SELECT c.Ciudad, COALESCE(SUM(v.ImporteVenta),0) AS importe_total, COALESCE(SUM(v.Cantidad),0) AS unidades FROM [dw].[Fact_Ventas] v JOIN [dw].[Dim_Cliente] c ON v.ClienteKey=c.ClienteKey GROUP BY c.Ciudad ORDER BY importe_total DESC",
    }

    def get(self, request, report):
        query = self.QUERIES.get(report)
        if not query:
            return Response({"detail": "Reporte no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [column[0] for column in cursor.description]
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return Response({"reporte": report, "datos": rows})
