# Uso de MySql

## Instalar MySql de manera local

### En Windows

1. Comenzar instalacion de MySql (8.0.41)
[Enlace de MySql (8.0.41)](https://dev.mysql.com/downloads/file/?id=536787)

2. Seleccionar "Server only".

3. Configurar un usuario **Root** y un puerto (por defecto, Port: 3306 y X Protocol Port: 33060).

4. Elegir y confirmar password para user Root. Propongo usar **G!8sD7&jVq2Z6lW**

5. Elegir nombre del servicio de MySql. En mi caso **MySQL80**

6. Finalizar la instalación y asegúrate de que MySQL Server esté corriendo.

7. Abrir la aplicacion **MySQL 8.0 Command Line Client** y conectarse a MySQL como root

### En Ubuntu/Debian (falta probar si anda)

1. Actualizar el sistema:

```bash
sudo apt update
sudo apt upgrade
```

2. Instalar MySQL Server:

```bash
sudo apt install mysql-server
```

3. Configurar MySQL:

```bash
sudo mysql_secure_installation
```

En la terminal se te pregunta: Set root password? [Y/n]
- Seleccionar [Y] y elegir una password
- Luego dar [Y] a todo.

4. Verificar estado de MySQL:

```bash
sudo systemctl status mysql
```

5. Conectarte a MySQL como root:

```bash
sudo mysql -u root -p 
```

## Conectar a un MySQL remoto (Sin necesidad de instalar en MySQL en PC personal, esto lo haremos en un futuro para el hosting)

Aunque todavia no lo haremos, debe ser algo como

```python
import mysql.connector

conn = mysql.connector.connect(
    host="tu-host-remoto",
    user="tu-usuario",
    password="tu-contraseña",
    database="tu-base-de-datos",
    port=3306  # Puede variar según el hosting
)

cursor = conn.cursor()
cursor.execute("SELECT DATABASE();")
print(cursor.fetchone())  # Verifica que estás conectado
```
