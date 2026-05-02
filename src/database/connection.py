import mysql.connector
from mysql.connector import Error
from datetime import datetime
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
            # Filtramos donde la fecha sea mayor o igual a "ahora"
            sql = "SELECT * FROM vista_agenda_completa WHERE Fecha_Raw >= NOW()"
            cursor.execute(sql)
            res = cursor.fetchall()
            cursor.close()
            conexion.close()
            return res
        return []

    def registrar_reserva(self, id_cliente, id_empleado, id_servicio, fecha_usuario):
        try:
            # 1. TRADUCCIÓN: Convertimos lo que vos escribís a algo que MySQL entienda
            # Esperamos: "17/03/2026 16:00"
            fecha_dt = datetime.strptime(fecha_usuario, '%d/%m/%Y %H:%M')
            
            # 2. FORMATO BD: Lo pasamos a "2026-03-17 16:00:00"
            fecha_para_mysql = fecha_dt.strftime('%Y-%m-%d %H:%M:%S')

            conexion = self.conectar()
            if conexion:
                cursor = conexion.cursor()
                sql = """INSERT INTO reserva (cliente_idcliente, empleado_idempleado, 
                         servicio_idservicio, fecha_inicio, estado) 
                         VALUES (%s, %s, %s, %s, 'pendiente')"""
                
                # Usamos la fecha ya convertida
                valores = (id_cliente, id_empleado, id_servicio, fecha_para_mysql)
                
                cursor.execute(sql, valores)
                conexion.commit()
                cursor.close()
                conexion.close()
                return True
        except Exception as e:
            # Si el usuario escribe mal el formato (ej: pone letras), salta acá
            print(f"Error de formato o BD: {e}")
            return False

    def obtener_o_crear_cliente(self, nombre_cliente):
        conexion = self.conectar()
        if conexion:
            cursor = conexion.cursor(dictionary=True)
            try:
                # 1. Buscamos si ya existe una persona con ese nombre
                cursor.execute("SELECT c.idcliente FROM cliente c JOIN persona p ON c.persona_idpersona = p.idpersona WHERE p.nombre = %s", (nombre_cliente,))
                resultado = cursor.fetchone()
                
                if resultado:
                    return resultado['idcliente']
                
                # 2. Si no existe, creamos la persona primero
                cursor.execute("INSERT INTO persona (nombre) VALUES (%s)", (nombre_cliente,))
                id_persona = cursor.lastrowid
                
                # 3. Luego lo creamos como cliente
                cursor.execute("INSERT INTO cliente (persona_idpersona) VALUES (%s)", (id_persona,))
                id_nuevo_cliente = cursor.lastrowid
                
                conexion.commit()
                return id_nuevo_cliente
            except Error as e:
                print(f"Error al gestionar cliente: {e}")
                return None
            finally:
                cursor.close()
                conexion.close()
        return None

    def obtener_empleados(self):
        conexion = self.conectar()
        if conexion:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT e.idempleado, p.nombre FROM empleado e JOIN persona p ON e.persona_idpersona = p.idpersona")
            res = cursor.fetchall()
            cursor.close()
            conexion.close()
            return res
        return []

    def obtener_servicios(self):
        conexion = self.conectar()
        if conexion:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT idservicio, nombre FROM servicio")
            res = cursor.fetchall()
            cursor.close()
            conexion.close()
            return res
        return []