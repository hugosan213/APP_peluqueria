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
            # (Mantener la lógica de conversión de fecha que ya tenemos)
            formatos = ['%d/%m/%Y %H:%M:%S', '%d/%m/%Y %H:%M', '%d/%m/%Y']
            fecha_dt = next((datetime.strptime(fecha_usuario, f) for f in formatos if True), None)
            # ... (Validaciones de fecha)
            fecha_mysql = fecha_dt.strftime('%Y-%m-%d %H:%M:%S')

            conexion = self.conectar()
            if conexion:
                cursor = conexion.cursor(dictionary=True)
                
                # VALIDACIÓN: Buscar si el empleado ya tiene un turno en esa fecha/hora
                sql_check = "SELECT idreserva FROM reserva WHERE empleado_idempleado = %s AND fecha_inicio = %s"
                cursor.execute(sql_check, (id_empleado, fecha_mysql))
                
                if cursor.fetchone():
                    print("¡Error! El peluquero ya tiene un turno a esa hora.")
                    return False # Aquí podrías lanzar una alerta en la UI más adelante
                
                # Si está libre, insertamos
                sql_ins = """INSERT INTO reserva (cliente_idcliente, empleado_idempleado, 
                             servicio_idservicio, fecha_inicio, estado) 
                             VALUES (%s, %s, %s, %s, 'pendiente')"""
                cursor.execute(sql_ins, (id_cliente, id_empleado, id_servicio, fecha_mysql))
                conexion.commit()
                return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def obtener_o_crear_cliente(self, nombre, apellido, email):
        conexion = self.conectar()
        if conexion:
            cursor = conexion.cursor(dictionary=True)
            try:
                # Buscamos por email (el cliente no necesita dar su DNI)
                cursor.execute("""SELECT c.idcliente FROM cliente c 
                                  JOIN persona p ON c.persona_idpersona = p.idpersona 
                                  WHERE p.email = %s""", (email,))
                resultado = cursor.fetchone()
                if resultado: return resultado['idcliente']
                
                # Si es nuevo, creamos la persona (sin campo DNI)
                cursor.execute("INSERT INTO persona (nombre, apellido, email) VALUES (%s, %s, %s)", 
                               (nombre, apellido, email))
                id_p = cursor.lastrowid
                cursor.execute("INSERT INTO cliente (persona_idpersona) VALUES (%s)", (id_p,))
                conexion.commit()
                return cursor.lastrowid
            except Exception as e:
                print(f"Error cliente: {e}")
            finally:
                cursor.close(); conexion.close()
        return None

    def agregar_empleado(self, nombre, apellido, email, dni):
        conexion = self.conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                # Insertamos a la persona con su DNI
                sql = "INSERT INTO persona (nombre, apellido, email, dni) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (nombre, apellido, email, dni))
                id_p = cursor.lastrowid
                
                cursor.execute("INSERT INTO empleado (persona_idpersona) VALUES (%s)", (id_p,))
                conexion.commit()
                return True
            except Exception as e:
                print(f"Error empleado: {e}")
            finally:
                cursor.close(); conexion.close()
        return False

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

    def agregar_empleado(self, nombre, apellido, email):
        conexion = self.conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                # 1. Crear persona con datos completos
                cursor.execute("INSERT INTO persona (nombre, apellido, email) VALUES (%s, %s, %s)", 
                               (nombre, apellido, email))
                id_p = cursor.lastrowid
                # 2. Crear el registro en la tabla empleado
                cursor.execute("INSERT INTO empleado (persona_idpersona) VALUES (%s)", (id_p,))
                conexion.commit()
                return True
            except Exception as e:
                print(f"Error empleado: {e}")
            finally:
                cursor.close()
                conexion.close()
        return False