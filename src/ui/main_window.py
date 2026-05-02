import customtkinter as ctk
from database.connection import Database

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana
        self.title("Peluquería - Gestión de Turnos")
        self.geometry("800x500")
        ctk.set_appearance_mode("System") 
        ctk.set_default_color_theme("blue")

        # Título principal
        self.label_titulo = ctk.CTkLabel(self, text="Agenda de Hoy", font=("Roboto", 24, "bold"))
        self.label_titulo.pack(pady=20)

        # Contenedor para los turnos
        self.frame_agenda = ctk.CTkFrame(self)
        self.frame_agenda.pack(pady=10, padx=20, fill="both", expand=True)

        # Botón para actualizar datos
        self.btn_actualizar = ctk.CTkButton(self, text="Actualizar Agenda", command=self.cargar_datos)
        self.btn_actualizar.pack(pady=20)

        # Botón para abrir formulario de nuevo turno
        self.btn_nuevo = ctk.CTkButton(self, text="Nueva Reserva +", 
                                       fg_color="green", hover_color="darkgreen",
                                       command=self.abrir_formulario)
        self.btn_nuevo.pack(pady=10)

        # Cargar datos al iniciar
        self.cargar_datos()

    def cargar_datos(self):
        for widget in self.frame_agenda.winfo_children():
            widget.destroy()

        db = Database()
        turnos = db.obtener_agenda()

        if not turnos:
            label_error = ctk.CTkLabel(self.frame_agenda, text="No hay turnos registrados.")
            label_error.pack(pady=10)
        else:
            header = ctk.CTkLabel(self.frame_agenda, text="FECHA | CLIENTE | SERVICIO | PELUQUERO", font=("Roboto", 12, "bold"))
            header.pack(pady=5)

            # En la función cargar_datos de main_window.py
            for t in turnos:
                # Usamos Fecha_Hora que es la que tiene el formato DD/MM HH:MM
                texto = f"{t['Fecha_Hora']} - {t['Cliente']} - {t['Servicio']} - {t['Peluquero']}"
                lbl = ctk.CTkLabel(self.frame_agenda, text=texto)
                lbl.pack(pady=2)

    def abrir_formulario(self):
        ventana_registro = ctk.CTkToplevel(self)
        ventana_registro.title("Registrar Nuevo Turno")
        ventana_registro.geometry("500x600")
        ventana_registro.attributes("-topmost", True)

        from datetime import datetime
        db = Database()
        
        # Cargamos datos para los combos
        lista_empleados = db.obtener_empleados()
        lista_servicios = db.obtener_servicios()
        nombres_empleados = [e['nombre'] for e in lista_empleados]
        nombres_servicios = [s['nombre'] for s in lista_servicios]

        # --- INTERFAZ ---
        ctk.CTkLabel(ventana_registro, text="Nombre del Cliente:").pack(pady=5)
        entry_cliente = ctk.CTkEntry(ventana_registro, width=300)
        entry_cliente.pack()

        ctk.CTkLabel(ventana_registro, text="Peluquero/a:").pack(pady=5)
        combo_empleado = ctk.CTkComboBox(ventana_registro, values=nombres_empleados, width=300)
        combo_empleado.pack()

        ctk.CTkLabel(ventana_registro, text="Servicio:").pack(pady=5)
        combo_servicio = ctk.CTkComboBox(ventana_registro, values=nombres_servicios, width=300)
        combo_servicio.pack()

        # --- SECCIÓN FECHA Y HORA ---
        ctk.CTkLabel(ventana_registro, text="Fecha (DD/MM/AAAA):").pack(pady=5)
        # Ponemos la fecha de hoy por defecto
        fecha_hoy = datetime.now().strftime("%d/%m/%Y")
        entry_fecha = ctk.CTkEntry(ventana_registro, width=300)
        entry_fecha.insert(0, fecha_hoy)
        entry_fecha.pack()

        # Contenedor para los selectores de hora
        frame_hora = ctk.CTkFrame(ventana_registro, fg_color="transparent")
        frame_hora.pack(pady=10)

        ctk.CTkLabel(frame_hora, text="Hora:").pack(side="left", padx=5)
        # Horas de 08 a 21 (típico de peluquería)
        horas_valores = [f"{i:02d}" for i in range(8, 22)]
        combo_hora = ctk.CTkComboBox(frame_hora, values=horas_valores, width=70)
        combo_hora.set("10") # Valor inicial
        combo_hora.pack(side="left", padx=5)

        ctk.CTkLabel(frame_hora, text="Min:").pack(side="left", padx=5)
        # Minutos de 15 en 15
        minutos_valores = ["00", "15", "30", "45"]
        combo_min = ctk.CTkComboBox(frame_hora, values=minutos_valores, width=70)
        combo_min.set("00")
        combo_min.pack(side="left", padx=5)

        def guardar():
            nombre_c = entry_cliente.get()
            # Armamos la fecha final uniendo los campos
            fecha_final = f"{entry_fecha.get()} {combo_hora.get()}:{combo_min.get()}"
            
            id_c = db.obtener_o_crear_cliente(nombre_c)
            id_e = next(e['idempleado'] for e in lista_empleados if e['nombre'] == combo_empleado.get())
            id_s = next(s['idservicio'] for s in lista_servicios if s['nombre'] == combo_servicio.get())

            if id_c and db.registrar_reserva(id_c, id_e, id_s, fecha_final):
                ventana_registro.destroy()
                self.cargar_datos()

        ctk.CTkButton(ventana_registro, text="Confirmar Turno", fg_color="blue", command=guardar).pack(pady=30)