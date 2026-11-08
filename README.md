# NicaGrow Django API (limpia)

API REST de solo lectura para el esquema `dw` de `nicagrow_dw`. Las tablas `staging` no están modeladas ni se consultan.

## Ejecutarla localmente

1. Abre la carpeta con PyCharm.
2. Copia `.env.example` como `.env`.
3. En `.env`, escribe tu contraseña en `DB_PASSWORD` y define un valor privado para `API_KEY`.
4. En PowerShell ejecuta `./Iniciar.ps1`, o configura el intérprete `.venv` en PyCharm y ejecuta `manage.py runserver`.
5. Comprueba `http://127.0.0.1:8000/healthz/` en el navegador.

Para los endpoints de `/api/`, incluye este encabezado:

```
X-Api-Key: el-valor-de-API_KEY
```

## Endpoints

- `GET /api/health/` confirma conexión a SQL Server.
- `GET /api/productos/`, `/api/clientes/`, `/api/ventas/` y el resto de las dimensiones y hechos DW.
- `GET /api/productos/?buscar=texto&pagina=1&tamano=50`
- `GET /api/ventas/?ClienteKey=1&orden=-ImporteVenta`
- `GET /api/reportes/resumen-ventas/`
- `GET /api/reportes/ventas-mensuales/`
- `GET /api/reportes/top-productos/`
- `GET /api/reportes/ventas-ciudad/`

No hay rutas `POST`, `PUT`, `PATCH` o `DELETE`: esta API protege el Data Warehouse como fuente de lectura.

## Azure App Service

Configura las variables de entorno equivalentes a `.env`, con `DEBUG=False` y añade el dominio de Azure en `ALLOWED_HOSTS`. En **Configuración general**, usa el comando de inicio:

```
gunicorn --bind=0.0.0.0:$PORT --workers=2 --timeout=120 config.wsgi:application
```

Para acceder al servidor Azure SQL desde App Service, habilita en el firewall de SQL la opción de servicios de Azure o agrega las IP salientes del App Service. La API seguirá respondiendo `503` mientras el firewall bloquee la conexión.
