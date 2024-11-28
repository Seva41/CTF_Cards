# CTF Cards

This project is a web application developed as part of the course IT Security - TICS413 2024/2 in Viña del Mar and Santiago, Chile. The application is designed to be used in a Capture The Flag (CTF) focused on IT security, applying encryption, hashing, SQL Injection, and XSS.

## Description

The web application allows users to interact with various security challenges. It is built using Flask, a Python microframework, and includes several security features such as CSRF protection, secure session management, and request rate limiting.

## Features

- **CSRF Protection**: Implemented with `Flask-WTF`.
- **Session Management**: Uses `Flask-Session` for server-side session handling.
- **Request Rate Limiting**:  Implemented with `Flask-Limiter`.
- **Secure Handling of Static Files**.
- **Custom Error Handling**: Error pages for codes 404, 429, 500, and 403.
- **Security Challenges**: Includes various flags that users must find.
  
## Requirements

- Python 3.10.11
- Flask
- Flask-WTF
- Flask-Session
- Flask-Limiter

## Installation

1. Clone the repository:
    ```sh
    git clone <URL_DEL_REPOSITORIO>
    cd <NOMBRE_DEL_REPOSITORIO>
    ```

2. Create a virtual environment and install the dependencies:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3. Set up the database:
    ```sh
    python create_database.py
    ```

4. Run the application:
    ```sh
    python app.py
    ```

## Deployment

To deploy this application in a production environment, consider the following changes:

1. **Secret Key Configuration**: Instead of generating a random secret key each time the application starts, set a fixed secret key in environment variables or a secure configuration file.
    ```py
    app.secret_key = os.getenv("SECRET_KEY", "default_secret_key")
    ```

2. **Database Configuration**: Ensure that the database is correctly configured and accessible from the production environment.

3. **HTTPS Configuration**: Make sure the application is behind a server that handles HTTPS, such as Nginx or Apache.

4. **Session Configuration**: Configure the appropriate session type for the production environment (e.g., Redis, Memcached).
    ```py
    app.config["SESSION_TYPE"] = "redis"
    app.config["SESSION_REDIS"] = redis.from_url("redis://localhost:6379")
    ```

5. **Log Management**: Set up log handling so that logs are stored persistently and are accessible for monitoring.
    ```py
    handler = RotatingFileHandler("error.log", maxBytes=10000, backupCount=1)
    handler.setLevel(logging.ERROR)
    app.logger.addHandler(handler)
    ```

## Author

Sebastián Dinator  
[https://sebadinator.com/](https://sebadinator.com/)  
November 2024
