# CTF Cards

Este proyecto es una aplicación web desarrollada como parte del curso Seguridad en TI TICS413 2024-2 en Viña del Mar y Santiago. La aplicación está diseñada para ser utilizada en un Capture The Flag (CTF) enfocado en la seguridad en TI, aplicando cifrado, hashing, SQL Injection y XSS.

## Descripción

La aplicación web permite a los usuarios interactuar con varios desafíos de seguridad. Está construida utilizando Flask, un microframework de Python, y cuenta con varias funcionalidades de seguridad como protección CSRF, manejo seguro de sesiones y limitación de tasa de solicitudes.

## Funcionalidades

- **Protección CSRF**: Implementada con `Flask-WTF`.
- **Manejo de sesiones**: Utiliza `Flask-Session` para manejar sesiones del lado del servidor.
- **Limitación de tasa de solicitudes**: Implementada con `Flask-Limiter`.
- **Manejo seguro de archivos estáticos**.
- **Manejo de errores personalizados**: Páginas de error para códigos 404, 429, 500 y 403.
- **Desafíos de seguridad**: Incluye varias banderas (`flags`) que los usuarios deben encontrar.

## Requisitos

- Python 3.10.11
- Flask
- Flask-WTF
- Flask-Session
- Flask-Limiter

## Instalación

1. Clona el repositorio:
    ```sh
    git clone <URL_DEL_REPOSITORIO>
    cd <NOMBRE_DEL_REPOSITORIO>
    ```

2. Crea un entorno virtual e instala las dependencias:
    ```sh
    python -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3. Configura la base de datos:
    ```sh
    python create_database.py
    ```

4. Ejecuta la aplicación:
    ```sh
    python app.py
    ```

## Despliegue

Para desplegar esta aplicación en un entorno de producción, se deben considerar los siguientes cambios:

1. **Configuración de la clave secreta**: En lugar de generar una clave secreta aleatoria cada vez que se inicia la aplicación, se debe configurar una clave secreta fija en las variables de entorno o en un archivo de configuración seguro.
    ```py
    app.secret_key = os.getenv("SECRET_KEY", "default_secret_key")
    ```

2. **Configuración de la base de datos**: Asegúrate de que la base de datos esté configurada correctamente y accesible desde el entorno de producción.

3. **Configuración de HTTPS**: Asegúrate de que la aplicación esté detrás de un servidor que maneje HTTPS, como Nginx o Apache.

4. **Configuración de sesiones**: Configura el tipo de sesión adecuado para el entorno de producción (por ejemplo, Redis, Memcached, etc.).
    ```py
    app.config["SESSION_TYPE"] = "redis"
    app.config["SESSION_REDIS"] = redis.from_url("redis://localhost:6379")
    ```

5. **Manejo de logs**: Configura el manejo de logs para que se almacenen de manera persistente y sean accesibles para monitoreo.
    ```py
    handler = RotatingFileHandler("error.log", maxBytes=10000, backupCount=1)
    handler.setLevel(logging.ERROR)
    app.logger.addHandler(handler)
    ```

## Autor

Sebastián Dinator  
[https://sebadinator.com/](https://sebadinator.com/)  
Noviembre 2024