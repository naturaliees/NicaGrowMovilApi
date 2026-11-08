if (-not (Test-Path .venv)) { py -m venv .venv }
& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
if (-not (Test-Path .env)) { Copy-Item .env.example .env; Write-Host "Edita .env y agrega DB_PASSWORD y API_KEY." -ForegroundColor Yellow }
& .\.venv\Scripts\python.exe manage.py runserver
