
# 1. Instalar MySql (La primera vez)

Seguir las instrucciones de Documentation/mysql.md

# 2. Crear un entorno virtual (La primera vez).

```bash
python venv .venv
```

# 3. Activar entorno virtual (Siempre): 

```bash
source .venv/Scripts/activate
``` 
en Windows

```bash
source .venv/bin/activate
``` 
en Debian/Ubuntu

# 4. Instalar requerimientos (La primera vez):

```bash
pip install -r requeriments.txt
```

# 5. Crear variables de entorno (La primera vez):

- Crear un archivo llamado **.env** en la ubicacion

e-commerce-server/
│
├── .env                          # Archivo de variables de entorno
│

- Escribir

GOOGLE_CLIENT_ID=you_google_client_id
DB_NAME=you_db_name
DB_USER=your_db_user
DB_PASSWORD=you_db_password
DB_HOST=your_db_host
DB_PORT=you_db_port

reemplazando por los valores correspondientes (sin usar comillas)

# 6. Crear base de datos  (La primera vez):

```bash
python -m src.app.database.create_db
```

# 7. Generar un sript de migracion  (La primera vez y cuando actualizas algun sqlalchemy model):

```bash
alembic revision --autogenerate -m "migration name"
```

# 8. Aplicar la migración (La primera vez y cuando actualizas algun sqlalchemy model):

```bash
alembic upgrade head
```

# 9. Levantar servidor (Siempre):

```bash
uvicorn src.app.main:app --reload
```
