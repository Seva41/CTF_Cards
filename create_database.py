import sqlite3

# Conectar a la base de datos (se creará si no existe)
con = sqlite3.connect('database.db')
cur = con.cursor()

# Crear la tabla de usuarios
cur.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    );
''')

# Insertar datos de prueba
cur.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin123')")
cur.execute("INSERT INTO users (username, password) VALUES ('user', 'userpass')")

# Confirmar los cambios y cerrar la conexión
con.commit()
con.close()

print("Base de datos creada exitosamente.")
