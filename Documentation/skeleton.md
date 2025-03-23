e-commerce-server/
│
├── alembic/                      # Carpeta con las migraciones de Alembic (para gestión de esquemas de base de datos)
│   ├── versions/                 # Carpeta donde se almacenan las migraciones de la base de datos
│   ├── env.py                    # Configuración de Alembic y conexión a la BD
│   ├── script.py.mako            # Plantilla para generar nuevas migraciones
│
├── Documentation/                # Directorio con markdowns con documentación 
│
├── src/                          # Código fuente de la aplicación
│   ├── app/                      # Carpeta principal de la aplicación
│   │   │ 
│   │   ├── models/               # Modelos de la base de datos (definiciones de tablas y relaciones)
│   │   │   ├── __init__.py       # Inicialización del paquete
│   │   │   ├── user.py           # Modelo de usuario (representa la tabla de usuarios en la base de datos)
│   │   ├── schemas/              # Esquemas de Pydantic (definiciones de datos para la validación de entrada/salida)
│   │   │   ├── __init__.py       # Inicialización del paquete
│   │   │   ├── user.py           # Esquema de usuario (definiciones para la validación de datos del usuario)
│   │   │   ├── token.py          # Esquema para el token de autenticación (puede ser el token de Google, JWT, etc.)
│   │   ├── crud/                 # Funciones CRUD (operaciones básicas sobre la base de datos)
│   │   │   ├── __init__.py       # Inicialización del paquete
│   │   │   ├── user.py           # Funciones CRUD para usuarios (como crear, leer, actualizar, eliminar usuarios)
│   │   ├── database/             # Configuración de la base de datos
│   │   │   ├── __init__.py       # Inicialización del paquete
│   │   │   ├── session.py        # Manejo de la sesión de la base de datos (creación y cierre de conexiones)
│   │   │   ├── create_db.py      # Script para crear la base de datos si no existe (puedes usar esto al iniciar el proyecto)
│   │   ├── api/                  # Rutas API (manejo de las rutas y vistas de la aplicación)
│   │   │   ├── __init__.py       # Inicialización del paquete
│   │   │   ├── auth.py           # Rutas de autenticación (para login, registro, manejo de tokens, etc.)
│   │   ├── __init__.py           # Inicialización del paquete (para importar módulos dentro de 'app')
│   │   ├── main.py               # Punto de entrada de la aplicación, como el archivo donde se ejecuta FastAPI o el servidor
│   │   └── config.py             # Configuración general (variables globales, configuración de terceros, etc.)
│
├── requirements.txt              # Dependencias del proyecto (todas las librerías necesarias para ejecutar el proyecto)
│
├── .gitignore                    # Archivos y directorios que deben ser ignorados por Git (como dependencias, configuraciones locales, etc.)
│
├── alembic.ini                   # Archivo de configuración de Alembic (para manejar las migraciones de la base de datos)
│
├── .env                          # Archivo de variables de entorno (con datos sensibles como contraseñas, claves API, etc.)
│
