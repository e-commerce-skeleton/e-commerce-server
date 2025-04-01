e-commerce-server/
│
├── alembic/                                # Carpeta con las migraciones de Alembic (para gestión de esquemas de base de datos)
│   ├── versions/                           # Carpeta donde se almacenan las migraciones de la base de datos
│   ├── env.py                              # Configuración de Alembic y conexión a la BD
│   ├── script.py.mako                      # Plantilla para generar nuevas migraciones
│           
├── Documentation/                          # Directorio con archivos markdowns con documentación sobre la API, base de datos, y otros aspectos del proyecto
│   ├── API_Documentation.md                # Documentación de los endpoints disponibles en la API
│   ├── Database_Schema.md                  # Explicación sobre el modelo de la base de datos y sus relaciones
│   ├── Setup_Guide.md                      # Instrucciones para instalar y ejecutar el proyecto
│           
├── src/                                    # Código fuente de la aplicación
│   ├── app/                                # Carpeta principal de la aplicación
│       │           
│       ├── models/                         # Modelos de la base de datos (definiciones de tablas y relaciones)
│       │   ├── init.py                     # Inicialización del paquete
│       │   ├── user.py                     # Modelo de usuario (representa la tabla de usuarios en la base de datos)
│       │   ├── category.py                 # Modelo de categoría de productos
│       │   ├── product.py                  # Modelo de productos
│       │   ├── product_category.py         # Tabla intermedia para la relación muchos-a-muchos entre productos y categorías
│       │
│       ├── schemas/                        # Esquemas de Pydantic (definiciones de datos para validación de entrada/salida)
│       │   ├── init.py                     # Inicialización del paquete
│       │   ├── user.py                     # Esquema para validación de datos del usuario
│       │   ├── category.py                 # Esquema para validación de datos de categorías
│       │   ├── product.py                  # Esquema para validación de datos de productos
│       │   ├── token.py                    # Esquema para manejo de tokens de autenticación (JWT, OAuth, etc.)
│       │           
│       ├── crud/                           # Funciones CRUD (operaciones básicas sobre la base de datos)
│       │   ├── init.py                     # Inicialización del paquete
│       │   ├── user.py                     # Funciones CRUD para usuarios
│       │   ├── category.py                 # Funciones CRUD para categorías
│       │   ├── product.py                  # Funciones CRUD para productos
│       │           
│       ├── database/                       # Configuración y gestión de la base de datos
│       │   ├── init.py                     # Inicialización del paquete
│       │   ├── session.py                  # Manejo de la sesión de la base de datos (creación y cierre de conexiones)
│       │   ├── create_db.py                # Script para crear la base de datos si no existe
│       │           
│       ├── api/                            # Rutas API (manejo de los endpoints de la aplicación)
│       │   ├── init.py                     # Inicialización del paquete
│       │   ├── auth.py                     # Rutas de autenticación (login, registro, manejo de tokens)
│       │   ├── product.py                  # Rutas relacionadas con el stock de productos
│       │           
│       ├── init.py                         # Inicialización del paquete (para importar módulos dentro de 'app')
│       ├── main.py                         # Punto de entrada de la aplicación (inicializa FastAPI y carga la configuración)
│       ├── config.py                       # Configuración general (variables globales, configuración de terceros, etc.)
│           
├── tests/                                  # Directorio para pruebas automáticas (unitarias e integraciones)
│   ├── init.py                             # Inicialización del paquete
│   ├── test_auth.py                        # Pruebas para autenticación y seguridad
│   ├── test_products.py                    # Pruebas para la funcionalidad de productos
│   ├── test_categories.py                  # Pruebas para la funcionalidad de categorías
│   ├── conftest.py                         # Configuración de pruebas y fixtures de pytest
│           
├── requirements.txt                        # Dependencias del proyecto (librerías necesarias para ejecutar la aplicación)
│           
├── .gitignore                              # Archivos y directorios ignorados por Git (como dependencias, configuraciones locales, etc.)
│           
├── alembic.ini                             # Archivo de configuración de Alembic (para manejar las migraciones de la base de datos)
│           
├── .env                                    # Archivo de variables de entorno (con datos sensibles como contraseñas, claves API, etc.)
│           
├── Dockerfile                              # Archivo para construir una imagen Docker del proyecto
│       
├── docker-compose.yml                      # Configuración de servicios Docker para el proyecto (base de datos, aplicación, etc.)
│       
└── README.md                               # Documentación general sobre el proyecto (qué hace, cómo instalarlo y ejecutarlo)