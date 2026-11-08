from django.db import models


class WarehouseModel(models.Model):
    class Meta:
        abstract = True
        managed = False


class DimCiudad(WarehouseModel):
    CiudadKey = models.AutoField(primary_key=True)
    CiudadID = models.CharField(max_length=3)
    Ciudad = models.CharField(max_length=50)
    class Meta(WarehouseModel.Meta): db_table = "[dw].[Dim_Ciudad]"


class DimCliente(WarehouseModel):
    ClienteKey = models.AutoField(primary_key=True)
    IdClienteOrigen = models.IntegerField()
    NombreCompleto = models.CharField(max_length=101)
    Ciudad = models.CharField(max_length=50, null=True)
    class Meta(WarehouseModel.Meta): db_table = "[dw].[Dim_Cliente]"


class DimEstado(WarehouseModel):
    EstadoKey = models.AutoField(primary_key=True)
    IdEstadoOrigen = models.IntegerField()
    TipoEstado = models.CharField(max_length=50)
    class Meta(WarehouseModel.Meta): db_table = "[dw].[Dim_Estado]"


class DimMetodoEnvio(WarehouseModel):
    MetodoEnvioKey = models.AutoField(primary_key=True)
    IdMetodoEnvioOrigen = models.IntegerField()
    MetodoEnvio = models.CharField(max_length=100)
    class Meta(WarehouseModel.Meta): db_table = "[dw].[Dim_Metodo_Envio]"


class DimMetodoPago(WarehouseModel):
    MetodoPagoKey = models.AutoField(primary_key=True)
    IdMetodoPagoOrigen = models.IntegerField()
    Metodo = models.CharField(max_length=100)
    class Meta(WarehouseModel.Meta): db_table = "[dw].[Dim_Metodo_Pago]"


class DimProducto(WarehouseModel):
    ProductoKey = models.AutoField(primary_key=True)
    IdProductoOrigen = models.IntegerField()
    NombreProducto = models.CharField(max_length=100)
    Categoria = models.CharField(max_length=100)
    class Meta(WarehouseModel.Meta): db_table = "[dw].[Dim_Producto]"


class DimTemporada(WarehouseModel):
    TemporadaKey = models.AutoField(primary_key=True)
    TemporadaID = models.IntegerField()
    NombreTemporada = models.CharField(max_length=100)
    class Meta(WarehouseModel.Meta): db_table = "[dw].[Dim_Temporada]"


class DimTiempo(WarehouseModel):
    TiempoKey = models.AutoField(primary_key=True)
    Fecha = models.DateField()
    Dia = models.IntegerField()
    Mes = models.IntegerField()
    Anio = models.IntegerField()
    class Meta(WarehouseModel.Meta): db_table = "[dw].[Dim_Tiempo]"


class DimVendedor(WarehouseModel):
    VendedorKey = models.AutoField(primary_key=True)
    IdVendedorOrigen = models.IntegerField()
    NombreCompleto = models.CharField(max_length=101)
    NombreNegocio = models.CharField(max_length=100)
    Ciudad = models.CharField(max_length=50, null=True)
    class Meta(WarehouseModel.Meta): db_table = "[dw].[Dim_Vendedor]"


class FactBusquedas(WarehouseModel):
    BusquedaKey = models.BigAutoField(primary_key=True)
    IdBusquedaOrigen = models.IntegerField()
    TiempoKey = models.ForeignKey(DimTiempo, db_column="TiempoKey", on_delete=models.DO_NOTHING, related_name="+")
    ClienteKey = models.ForeignKey(DimCliente, db_column="ClienteKey", on_delete=models.DO_NOTHING, related_name="+")
    ProductoKey = models.ForeignKey(DimProducto, db_column="ProductoKey", on_delete=models.DO_NOTHING, related_name="+")
    CantidadResultados = models.IntegerField()
    class Meta(WarehouseModel.Meta): db_table = "[dw].[Fact_Busquedas]"


class FactIncidentes(WarehouseModel):
    IncidenteKey = models.BigAutoField(primary_key=True)
    IdIncidenteOrigen = models.IntegerField()
    PedidoOrigen = models.IntegerField()
    TiempoKey = models.ForeignKey(DimTiempo, db_column="TiempoKey", on_delete=models.DO_NOTHING, related_name="+")
    ClienteKey = models.ForeignKey(DimCliente, db_column="ClienteKey", on_delete=models.DO_NOTHING, related_name="+")
    ProductoKey = models.ForeignKey(DimProducto, db_column="ProductoKey", on_delete=models.DO_NOTHING, related_name="+")
    CiudadKey = models.ForeignKey(DimCiudad, db_column="CiudadKey", on_delete=models.DO_NOTHING, related_name="+")
    MetodoEnvioKey = models.ForeignKey(DimMetodoEnvio, db_column="MetodoEnvioKey", on_delete=models.DO_NOTHING, related_name="+")
    CantidadIncidentes = models.IntegerField()
    class Meta(WarehouseModel.Meta): db_table = "[dw].[Fact_Incidentes]"


class FactTendenciaTemporada(WarehouseModel):
    TendenciaKey = models.BigAutoField(primary_key=True)
    IdTendenciaOrigen = models.IntegerField()
    TemporadaKey = models.ForeignKey(DimTemporada, db_column="TemporadaKey", on_delete=models.DO_NOTHING, related_name="+")
    ProductoKey = models.ForeignKey(DimProducto, db_column="ProductoKey", on_delete=models.DO_NOTHING, related_name="+")
    CantidadBusqueda = models.IntegerField()
    CantidadPedidos = models.IntegerField()
    class Meta(WarehouseModel.Meta): db_table = "[dw].[Fact_Tendencia_Temporada]"


class FactValoraciones(WarehouseModel):
    ValoracionKey = models.BigAutoField(primary_key=True)
    IdValoracionOrigen = models.IntegerField()
    TiempoKey = models.ForeignKey(DimTiempo, db_column="TiempoKey", on_delete=models.DO_NOTHING, related_name="+")
    ClienteKey = models.ForeignKey(DimCliente, db_column="ClienteKey", on_delete=models.DO_NOTHING, related_name="+")
    ProductoKey = models.ForeignKey(DimProducto, db_column="ProductoKey", on_delete=models.DO_NOTHING, related_name="+", null=True)
    MetodoEnvioKey = models.ForeignKey(DimMetodoEnvio, db_column="MetodoEnvioKey", on_delete=models.DO_NOTHING, related_name="+", null=True)
    Calificacion = models.IntegerField()
    class Meta(WarehouseModel.Meta): db_table = "[dw].[Fact_Valoraciones]"


class FactVentas(WarehouseModel):
    VentaKey = models.BigAutoField(primary_key=True)
    IdDetalleOrigen = models.IntegerField()
    IdPedidoOrigen = models.IntegerField()
    TiempoKey = models.ForeignKey(DimTiempo, db_column="TiempoKey", on_delete=models.DO_NOTHING, related_name="+")
    ClienteKey = models.ForeignKey(DimCliente, db_column="ClienteKey", on_delete=models.DO_NOTHING, related_name="+")
    ProductoKey = models.ForeignKey(DimProducto, db_column="ProductoKey", on_delete=models.DO_NOTHING, related_name="+")
    VendedorKey = models.ForeignKey(DimVendedor, db_column="VendedorKey", on_delete=models.DO_NOTHING, related_name="+")
    EstadoKey = models.ForeignKey(DimEstado, db_column="EstadoKey", on_delete=models.DO_NOTHING, related_name="+")
    MetodoPagoKey = models.ForeignKey(DimMetodoPago, db_column="MetodoPagoKey", on_delete=models.DO_NOTHING, related_name="+")
    MetodoEnvioKey = models.ForeignKey(DimMetodoEnvio, db_column="MetodoEnvioKey", on_delete=models.DO_NOTHING, related_name="+")
    Cantidad = models.IntegerField()
    PrecioUnitario = models.DecimalField(max_digits=10, decimal_places=2)
    ImporteVenta = models.DecimalField(max_digits=18, decimal_places=2)
    class Meta(WarehouseModel.Meta): db_table = "[dw].[Fact_Ventas]"
