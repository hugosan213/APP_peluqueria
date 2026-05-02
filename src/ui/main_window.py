import customtkinter as ctk
from database.connection import Database
from datetime import datetime

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Peluquería - Gestión Integral")
        self.geometry("1000x750")
        
        # --- CONFIGURACIÓN BASE CALIDA ---
        ctk.set_appearance_mode("Light") 
        self.configure(fg_color="#FAF9F6") # Blanco Crema Neutro

        # Estilo de las pestañas (Tabview) armonizado
        self.tabview = ctk.CTkTabview(self, 
                                      segmented_button_fg_color="#EADDCA", # Crema profundo
                                      segmented_button_selected_color="#5C4033", # Marrón café
                                      segmented_button_selected_hover_color="#3E2C23",
                                      text_color="black")
        self.tabview.pack(pady=10, padx=10, fill="both", expand=True)

        self.tab_agenda = self.tabview.add("Agenda de Hoy")
        self.tab_gestion = self.tabview.add("Configuración y Personal")

        # --- PESTAÑA 1: AGENDA ---
        
        # Sidebar interna
        self.sidebar_agenda = ctk.CTkFrame(self.tab_agenda, width=220, corner_radius=0, fg_color="#F2F0EB")
        self.sidebar_agenda.pack(side="left", fill="y")

        self.label_menu = ctk.CTkLabel(self.sidebar_agenda, text="ACCIONES", font=("Inter", 14, "bold"), text_color="#5C4033")
        self.label_menu.pack(pady=(30, 20), padx=10)

        self.btn_nuevo = ctk.CTkButton(self.sidebar_agenda, text="➕ Nueva Reserva", 
                                       fg_color="#6B8E23", hover_color="#556B2F", text_color="white", # Verde Oliva
                                       font=("Inter", 13, "bold"), height=40,
                                       command=self.abrir_formulario)
        self.btn_nuevo.pack(pady=10, padx=20, fill="x")

        self.btn_actualizar = ctk.CTkButton(self.sidebar_agenda, text="🔄 Actualizar", 
                                            fg_color="#A67B5B", hover_color="#8B5E3C", text_color="white", # Marrón suave
                                            font=("Inter", 13, "bold"), height=40,
                                            command=self.cargar_datos)
        self.btn_actualizar.pack(pady=10, padx=20, fill="x")

        self.linea_divisoria = ctk.CTkFrame(self.tab_agenda, width=1, fg_color="#E5E1DA")
        self.linea_divisoria.pack(side="left", fill="y")

        self.right_container = ctk.CTkFrame(self.tab_agenda, fg_color="#FAF9F6", corner_radius=0)
        self.right_container.pack(side="right", fill="both", expand=True)

        self.label_titulo = ctk.CTkLabel(self.right_container, text="Próximos Turnos", font=("Inter", 24, "bold"), text_color="#2D2424")
        self.label_titulo.pack(pady=20)

        self.frame_agenda = ctk.CTkScrollableFrame(self.right_container, fg_color="transparent")
        self.frame_agenda.pack(pady=10, padx=20, fill="both", expand=True)

        # --- PESTAÑA 2: GESTIÓN (REDISEÑADA) ---
        self.setup_tab_gestion()
        self.cargar_datos()

    def setup_tab_gestion(self):
        # Contenedor centrado para la gestión
        self.gestion_container = ctk.CTkFrame(self.tab_gestion, fg_color="#F2F0EB", corner_radius=15, border_width=1, border_color="#E5E1DA")
        self.gestion_container.pack(pady=50, padx=50, expand=True)

        ctk.CTkLabel(self.gestion_container, text="REGISTRAR NUEVO EMPLEADO", font=("Inter", 20, "bold"), text_color="#5C4033").pack(pady=(30, 20), padx=40)
        
        # Entradas con bordes que acompañan la paleta
        self.ent_emp_nom = ctk.CTkEntry(self.gestion_container, placeholder_text="Nombre", width=400, height=45, border_color="#D5D0C5")
        self.ent_emp_nom.pack(pady=10, padx=40)
        self.ent_emp_ape = ctk.CTkEntry(self.gestion_container, placeholder_text="Apellido", width=400, height=45, border_color="#D5D0C5")
        self.ent_emp_ape.pack(pady=10, padx=40)
        self.ent_emp_dni = ctk.CTkEntry(self.gestion_container, placeholder_text="DNI del Empleado (sin puntos)", width=400, height=45, border_color="#D5D0C5")
        self.ent_emp_dni.pack(pady=10, padx=40)
        self.ent_emp_mail = ctk.CTkEntry(self.gestion_container, placeholder_text="Email", width=400, height=45, border_color="#D5D0C5")
        self.ent_emp_mail.pack(pady=10, padx=40)

        # Botón de registro con el color de la marca
        self.btn_add_emp = ctk.CTkButton(self.gestion_container, text="Registrar Peluquero/a", 
                                         fg_color="#5C4033", hover_color="#3E2C23", width=250, height=50, font=("Inter", 14, "bold"),
                                         command=self.guardar_empleado)
        self.btn_add_emp.pack(pady=40)

    def guardar_empleado(self):
        db = Database()
        nom, ape, dni, mail = self.ent_emp_nom.get(), self.ent_emp_ape.get(), self.ent_emp_dni.get(), self.ent_emp_mail.get()
        if nom and ape and dni and mail:
            if db.agregar_empleado(nom, ape, mail, dni):
                for e in [self.ent_emp_nom, self.ent_emp_ape, self.ent_emp_dni, self.ent_emp_mail]: e.delete(0, 'end')

    def cargar_datos(self):
        for widget in self.frame_agenda.winfo_children(): widget.destroy()
        db = Database()
        turnos = db.obtener_agenda()

        if not turnos:
            ctk.CTkLabel(self.frame_agenda, text="No hay turnos registrados.", font=("Inter", 16), text_color="#A69F92").pack(pady=50)
        else:
            for t in turnos:
                card = ctk.CTkFrame(self.frame_agenda, corner_radius=12, border_width=1, border_color="#E5E1DA", fg_color="#FFFFFF")
                card.pack(fill="x", pady=6, padx=10)
                
                info_izq = f"🕒 {t['Fecha_Hora']}  |  👤 {t['Cliente']}"
                ctk.CTkLabel(card, text=info_izq, font=("Inter", 14, "bold"), text_color="#2D2424").pack(side="left", padx=20, pady=15)
                
                info_der = f"✂️ {t['Servicio']}  |  💈 {t['Peluquero']}"
                ctk.CTkLabel(card, text=info_der, font=("Inter", 13), text_color="#5C4033").pack(side="right", padx=20, pady=15)

    def abrir_formulario(self):
        ventana = ctk.CTkToplevel(self)
        ventana.title("Nueva Reserva")
        ventana.geometry("500x780")
        ventana.configure(fg_color="#FAF9F6")
        ventana.attributes("-topmost", True)

        db = Database()
        empleados = db.obtener_empleados()
        servicios = db.obtener_servicios()

        ctk.CTkLabel(ventana, text="DATOS DEL CLIENTE", font=("Inter", 16, "bold"), text_color="#2D2424").pack(pady=(25,15))
        e_nom = ctk.CTkEntry(ventana, placeholder_text="Nombre", width=380, height=40, border_color="#D5D0C5"); e_nom.pack(pady=5)
        e_ape = ctk.CTkEntry(ventana, placeholder_text="Apellido", width=380, height=40, border_color="#D5D0C5"); e_ape.pack(pady=5)
        e_mail = ctk.CTkEntry(ventana, placeholder_text="Email", width=380, height=40, border_color="#D5D0C5"); e_mail.pack(pady=5)

        ctk.CTkLabel(ventana, text="DETALLES DEL TURNO", font=("Inter", 16, "bold"), text_color="#2D2424").pack(pady=(25,15))
        c_emp = ctk.CTkComboBox(ventana, values=[e['nombre'] for e in empleados], width=380, height=40, border_color="#D5D0C5", button_color="#A67B5B"); c_emp.pack(pady=5)
        c_ser = ctk.CTkComboBox(ventana, values=[s['nombre'] for s in servicios], width=380, height=40, border_color="#D5D0C5", button_color="#A67B5B"); c_ser.pack(pady=5)

        e_fec = ctk.CTkEntry(ventana, width=380, height=40, border_color="#D5D0C5")
        e_fec.insert(0, datetime.now().strftime("%d/%m/%Y")); e_fec.pack(pady=15)

        f_h = ctk.CTkFrame(ventana, fg_color="transparent"); f_h.pack(pady=5)
        cb_h = ctk.CTkComboBox(f_h, values=[f"{i:02d}" for i in range(8,21)], width=85, height=40, border_color="#D5D0C5"); cb_h.set("10"); cb_h.pack(side="left", padx=5)
        cb_m = ctk.CTkComboBox(f_h, values=["00","15","30","45"], width=85, height=40, border_color="#D5D0C5"); cb_m.set("00"); cb_m.pack(side="left", padx=5)

        def guardar():
            id_c = db.obtener_o_crear_cliente(e_nom.get(), e_ape.get(), e_mail.get())
            try:
                id_e = next(e['idempleado'] for e in empleados if e['nombre'] == c_emp.get())
                id_s = next(s['idservicio'] for s in servicios if s['nombre'] == c_ser.get())
                fecha = f"{e_fec.get()} {cb_h.get()}:{cb_m.get()}"
                if db.registrar_reserva(id_c, id_e, id_s, fecha):
                    ventana.destroy(); self.cargar_datos()
            except: pass

        ctk.CTkButton(ventana, text="CONFIRMAR RESERVA", font=("Inter", 14, "bold"), 
                      fg_color="#6B8E23", hover_color="#556B2F", width=300, height=50,
                      command=guardar).pack(pady=40)