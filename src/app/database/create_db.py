from src.app.config import db_user, db_password, db_host, db_port, db_name
import pymysql
import os

# URL de conexión (sin el nombre de la base de datos)
DATABASE_URL = os.getenv("DATABASE_URL", f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}")

# Conectar al servidor MySQL (sin especificar base de datos)
conn = pymysql.connect(host=db_host, user=db_user, password=db_password, port=int(db_port))
cursor = conn.cursor()

# Verificar si la base de datos ya existe
cursor.execute("SHOW DATABASES")
databases = [db[0] for db in cursor.fetchall()]

if db_name not in databases:
    cursor.execute(f"CREATE DATABASE {db_name}")

# Cerrar la conexión
cursor.close()
conn.close()
