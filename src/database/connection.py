import mysql.connector
from mysql.connector import Error
from datetime import datetime

class Database:
    def __init__(self):
        self.config = {
            'host': '127.0.0.1',
            'user': 'root', 
            'password': '17032003Hsanti', 
            'database': 'peluqueria'
        }

    def conectar(self):
        try:
            conexion = mysql.connector.connect(**self.config)
            if conexion.is_connected():
                return conexion
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None

    # --- MÉTODOS DE SERVICIOS (ABM) ---
    def obtener_servicios_detallados(self):
        conexion = self.conectar()
        if conexion:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT idservicio, nombre, precio, duracion FROM servicio")
            res = cursor.fetchall()
            cursor.close(); conexion.close()
            return res
        return []

    # Método agregado para el ComboBox del formulario de reservas[cite: 10]
    def obtener_servicios(self):
        conexion = self.conectar()
        if conexion:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT idservicio, nombre FROM servicio")
            res = cursor.fetchall()
            cursor.close(); conexion.close()
            return res
        return []

    def agregar_servicio_nuevo(self, nombre, precio, duracion):
        conexion = self.conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                sql = "INSERT INTO servicio (nombre, precio, duracion) VALUES (%s, %s, %s)"
                cursor.execute(sql, (nombre, precio, duracion))
                conexion.commit()
                return True
            except Exception as e:
                print(f"Error al agregar servicio: {e}")
                return False
            finally:
                cursor.close(); conexion.close()
        return False
    

    def eliminar_servicio(self, id_servicio):
        conexion = self.conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                sql = "DELETE FROM servicio WHERE idservicio = %s"
                cursor.execute(sql, (id_servicio,))
                conexion.commit()
                return True
            except Exception:
                print("Error: No se puede eliminar un servicio que tiene turnos asociados.")
                return False
            finally:
                cursor.close(); conexion.close()
        return False

    def actualizar_servicio(self, id_servicio, precio, duracion):
        conexion = self.conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                sql = "UPDATE servicio SET precio = %s, duracion = %s WHERE idservicio = %s"
                cursor.execute(sql, (precio, duracion, id_servicio))
                conexion.commit()
                return True
            finally: cursor.close(); conexion.close()
        return False

    # --- MÉTODOS DE AGENDA Y COBRO ---
    def obtener_agenda(self):
        conexion = self.conectar()
        if conexion:
            cursor = conexion.cursor(dictionary=True)
            # Quitamos el filtro de tiempo estricto y priorizamos el estado
            sql = """SELECT * FROM vista_agenda_completa 
                     WHERE Estado = 'pendiente' 
                     ORDER BY Fecha_Raw ASC"""
            cursor.execute(sql)
            res = cursor.fetchall()
            cursor.close(); conexion.close()
            return res
        return []
    
    def obtener_historial_cortes(self):
        conexion = self.conectar()
        if conexion:
            cursor = conexion.cursor(dictionary=True)
            # Traemos los últimos 50 cortes realizados
            sql = """SELECT * FROM vista_agenda_completa 
                     WHERE Estado = 'finalizada' 
                     ORDER BY Fecha_Raw DESC LIMIT 50"""
            cursor.execute(sql)
            res = cursor.fetchall()
            cursor.close(); conexion.close()
            return res
        return []

    # Lógica de registro implementada[cite: 10]
    def registrar_reserva(self, id_cliente, id_empleado, id_servicio, fecha_sql):
        conexion = self.conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                sql = "INSERT INTO reserva (cliente_idcliente, empleado_idempleado, servicio_idservicio, fecha_inicio, estado) VALUES (%s, %s, %s, %s, 'pendiente')"
                cursor.execute(sql, (id_cliente, id_empleado, id_servicio, fecha_sql))
                conexion.commit()
                return True
            except Exception as e:
                print(f"Error al registrar reserva: {e}")
                return False
            finally: cursor.close(); conexion.close()
        return False

    def obtener_o_crear_cliente(self, nombre, apellido, mail):
        conexion = self.conectar()
        if conexion:
            cursor = conexion.cursor(dictionary=True)
            try:
                cursor.execute("SELECT c.idcliente FROM cliente c JOIN persona p ON c.persona_idpersona = p.idpersona WHERE p.mail = %s", (mail,))
                resultado = cursor.fetchone()
                if resultado: return resultado['idcliente']
                cursor.execute("INSERT INTO persona (nombre, apellido, mail) VALUES (%s, %s, %s)", (nombre, apellido, mail))
                id_p = cursor.lastrowid
                cursor.execute("INSERT INTO cliente (persona_idpersona) VALUES (%s)", (id_p,))
                conexion.commit()
                return cursor.lastrowid
            finally: cursor.close(); conexion.close()
        return None

    def obtener_clientes_lista(self):
        conexion = self.conectar()
        if conexion:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT c.idcliente, p.nombre, p.apellido, p.mail, c.notas_relevantes FROM cliente c JOIN persona p ON c.persona_idpersona = p.idpersona ORDER BY p.apellido ASC")
            res = res = cursor.fetchall()
            cursor.close(); conexion.close()
            return res
        return []

    def actualizar_notas_cliente(self, id_cliente, notas):
        conexion = self.conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                sql = "UPDATE cliente SET notas_relevantes = %s WHERE idcliente = %s"
                cursor.execute(sql, (notas, id_cliente))
                conexion.commit()
                return True
            finally: cursor.close(); conexion.close()
        return False

    def obtener_metodos_pago(self):
        conexion = self.conectar()
        if conexion:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT idmetodopago, tipoPago FROM metodo_pago")
            res = cursor.fetchall()
            cursor.close(); conexion.close()
            return res
        return []

    def finalizar_y_cobrar(self, id_reserva, monto, id_metodo):
        conexion = self.conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                cursor.execute("UPDATE reserva SET estado = 'finalizada', monto_total = %s WHERE idreserva = %s", (monto, id_reserva))
                cursor.execute("INSERT INTO pago (monto, fecha, metodo_pago_idmetodopago, reserva_idreserva) VALUES (%s, NOW(), %s, %s)", (monto, id_metodo, id_reserva))
                conexion.commit()
                return True
            finally: cursor.close(); conexion.close()
        return False

    def obtener_caja_diaria(self):
        conexion = self.conectar()
        if conexion:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT mp.tipoPago, SUM(p.monto) as total FROM pago p JOIN metodo_pago mp ON p.metodo_pago_idmetodopago = mp.idmetodopago WHERE DATE(p.fecha) = CURDATE() GROUP BY mp.tipoPago")
            res = cursor.fetchall()
            cursor.close(); conexion.close()
            return res
        return []

    # --- MÉTODO DE STOCK ---
    def obtener_productos_stock(self):
        conexion = self.conectar()
        if conexion:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT * FROM producto")
            res = cursor.fetchall()
            cursor.close(); conexion.close()
            return res
        return []

    def agregar_producto_stock(self, nombre, stock_actual, stock_minimo, unidad):
        conexion = self.conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                sql = "INSERT INTO producto (nombre, stock_actual, stock_minimo, unidad) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (nombre, stock_actual, stock_minimo, unidad))
                conexion.commit()
                return True
            except Exception as e:
                print(f"Error al agregar producto: {e}")
                return False
            finally:
                cursor.close(); conexion.close()
        return False

    # --- EMPLEADOS ---
    def obtener_empleados(self):
        conexion = self.conectar()
        if conexion:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT e.idempleado, p.nombre FROM empleado e JOIN persona p ON e.persona_idpersona = p.idpersona")
            res = cursor.fetchall()
            cursor.close(); conexion.close()
            return res
        return []

    def agregar_empleado(self, nombre, apellido, mail, dni):
        conexion = self.conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                sql_p = "INSERT INTO persona (nombre, apellido, mail, dni) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql_p, (nombre, apellido, mail, dni))
                id_persona = cursor.lastrowid
                cursor.execute("INSERT INTO empleado (persona_idpersona) VALUES (%s)", (id_persona,))
                conexion.commit()
                return True
            except Exception as e:
                print(f"Error al agregar empleado: {e}")
                return False
            finally: cursor.close(); conexion.close()
        return False

    def registrar_egreso(self, monto, descripcion):
        conexion = self.conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                sql = "INSERT INTO egreso (monto, descripcion) VALUES (%s, %s)"
                cursor.execute(sql, (monto, descripcion))
                conexion.commit()
                return True
            finally: cursor.close(); conexion.close()
        return False

    def obtener_total_egresos_hoy(self):
        conexion = self.conectar()
        if conexion:
            cursor = conexion.cursor(dictionary=True)
            # Sumamos todos los gastos del día actual
            cursor.execute("SELECT SUM(monto) as total FROM egreso WHERE DATE(fecha) = CURDATE()")
            res = cursor.fetchone()
            cursor.close(); conexion.close()
            return res['total'] if res['total'] else 0
        return 0

    def obtener_estadisticas_ingresos(self, periodo):
        conexion = self.conectar()
        if conexion:
            cursor = conexion.cursor(dictionary=True)
            # Definimos el formato según el periodo solicitado
            if periodo == "Semanal":
                # Agrupa por el número de semana del año[cite: 4]
                sql = "SELECT WEEK(fecha) as etiqueta, SUM(monto) as total FROM pago WHERE YEAR(fecha) = YEAR(NOW()) GROUP BY etiqueta"
            elif periodo == "Mensual":
                # Agrupa por nombre de mes[cite: 4]
                sql = "SELECT MONTHNAME(fecha) as etiqueta, SUM(monto) as total FROM pago WHERE YEAR(fecha) = YEAR(NOW()) GROUP BY etiqueta"
            else: # Anual
                sql = "SELECT YEAR(fecha) as etiqueta, SUM(monto) as total GROUP BY etiqueta"
            
            cursor.execute(sql)
            res = cursor.fetchall()
            cursor.close(); conexion.close()
            return res
        return []