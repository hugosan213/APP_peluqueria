import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        # Datos de tu servidor local en Esquel
        self.config = {
            'host': '127.0.0.1',
            'user': 'root', # Cambiá esto por tu usuario de MySQL
            'password': '17032003Hsanti', # Poné tu contraseña de MySQL
            'database': 'Peluqueria'
        }

    def conectar(self):
        try:
            conexion = mysql.connector.connect(**self.config)
            if conexion.is_connected():
                return conexion
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None

    def obtener_agenda(self):
        conexion = self.conectar()
        if conexion:
            cursor = conexion.cursor(dictionary=True)
            # Usamos la vista que creamos anteriormente en MySQL Workbench
            cursor.execute("SELECT * FROM vista_agenda_completa")
            resultados = cursor.fetchall()
            cursor.close()
            conexion.close()
            return resultados
        return []