import customtkinter as ctk
from database.connection import Database
from datetime import datetime

class AgendaTab:
    def __init__(self, master, parent):
        self.master = master  # Es el tab físico donde se dibuja todo
        self.parent = parent  # Es la ventana principal (MainWindow)
        self.db = Database()
        self.setup_ui()
        self.cargar_datos()

    def setup_ui(self):
        """Define la estructura visual de la pestaña agenda[cite: 7]"""
        self.sidebar = ctk.CTkFrame(self.master, width=220, fg_color="#F2F0EB")
        self.sidebar.pack(side="left", fill="y")
        
        ctk.CTkButton(self.sidebar, text="➕ Nueva Reserva", fg_color="#6B8E23", 
                      command=self.abrir_formulario).pack(pady=20, padx=20, fill="x")
        
        ctk.CTkButton(self.sidebar, text="🔄 Actualizar", fg_color="#A67B5B", 
                      command=self.cargar_datos).pack(pady=10, padx=20, fill="x")
        
        ctk.CTkButton(self.sidebar, text="📜 Ver Historial", fg_color="#5C4033", 
                      command=self.cargar_historial).pack(pady=10, padx=20, fill="x")
        
        self.frame_agenda = ctk.CTkScrollableFrame(self.master, fg_color="transparent")
        self.frame_agenda.pack(side="right", fill="both", expand=True, padx=20)

    def cargar_datos(self):
        """Refresca la lista de turnos activos[cite: 14]"""
        for widget in self.frame_agenda.winfo_children(): 
            widget.destroy()
            
        agenda = self.db.obtener_agenda()
        for t in agenda:
            card = ctk.CTkFrame(self.frame_agenda, fg_color="#FFFFFF", border_width=1, border_color="#E5E1DA", corner_radius=12)
            card.pack(fill="x", pady=6, padx=10)
            
            nombre_cliente = t.get('Cliente')
            if not nombre_cliente or str(nombre_cliente).strip() in ["", "None", "NULL"]:
                n = t.get('nombre', t.get('Nombre', ''))
                a = t.get('apellido', t.get('Apellido', ''))
                nombre_cliente = f"{n} {a}".strip() if (n or a) else "Cliente Nuevo"

            ctk.CTkLabel(card, text=f"🕒 {t['Fecha_Hora']} | 👤 {nombre_cliente}", 
                         font=("Inter", 14, "bold")).pack(side="left", padx=20, pady=15)

            if t.get('Estado') != 'finalizada':
                ctk.CTkButton(card, text="💵 Cobrar", width=80, fg_color="#6B8E23", 
                              command=lambda trn=t: self.abrir_ventana_cobro(trn)).pack(side="right", padx=10)
            
            ctk.CTkLabel(card, text=f"✂️ {t['Servicio']}", text_color="#5C4033").pack(side="right", padx=20)
        self.master.update_idletasks()

    def cargar_historial(self):
        """Muestra historial de cortes finalizados[cite: 14]"""
        for widget in self.frame_agenda.winfo_children(): widget.destroy()
        ctk.CTkLabel(self.frame_agenda, text="HISTORIAL DE CORTES FINALIZADOS", font=("Inter", 16, "bold")).pack(pady=10)
        
        for t in self.db.obtener_historial_cortes():
            card = ctk.CTkFrame(self.frame_agenda, fg_color="#E5E1DA", corner_radius=12)
            card.pack(fill="x", pady=6, padx=10)
            ctk.CTkLabel(card, text=f"🕒 {t['Fecha_Hora']} | 👤 {t['Cliente']}", font=("Inter", 14)).pack(side="left", padx=20, pady=15)
            ctk.CTkLabel(card, text=f"✅ {t['Servicio']}", text_color="#6B8E23", font=("Inter", 12, "italic")).pack(side="right", padx=20)
    
    def abrir_formulario(self):
        """Ventana para nueva reserva[cite: 7]"""
        v = ctk.CTkToplevel(self.master) # Cambiado a self.master
        v.title("NUEVA RESERVA")
        v.geometry("500x750")
        v.attributes("-topmost", True)
        v.configure(fg_color="#FAF9F6")

        empleados = self.db.obtener_empleados()
        servicios = self.db.obtener_servicios()

        ctk.CTkLabel(v, text="DATOS DEL CLIENTE", font=("Inter", 16, "bold"), text_color="#5C4033").pack(pady=(20, 10))
        en = ctk.CTkEntry(v, placeholder_text="Nombre", width=380); en.pack(pady=5)
        ea = ctk.CTkEntry(v, placeholder_text="Apellido", width=380); ea.pack(pady=5)
        em = ctk.CTkEntry(v, placeholder_text="Email (Opcional)", width=380); em.pack(pady=5)

        ctk.CTkLabel(v, text="DETALLES DEL TURNO", font=("Inter", 16, "bold"), text_color="#5C4033").pack(pady=(30, 10))
        cb_e = ctk.CTkComboBox(v, values=[e['nombre'] for e in empleados], width=380); cb_e.pack(pady=5)
        cb_s = ctk.CTkComboBox(v, values=[s['nombre'] for s in servicios], width=380); cb_s.pack(pady=5)

        ef = ctk.CTkEntry(v, width=380)
        ef.insert(0, datetime.now().strftime("%d/%m/%Y"))
        ef.pack(pady=5)

        f_h = ctk.CTkFrame(v, fg_color="transparent"); f_h.pack(pady=5)
        cb_h = ctk.CTkComboBox(f_h, values=[f"{i:02d}" for i in range(8, 21)], width=80); cb_h.set("10"); cb_h.pack(side="left", padx=5)
        cb_m = ctk.CTkComboBox(f_h, values=["00", "15", "30", "45"], width=80); cb_m.set("00"); cb_m.pack(side="left", padx=5)

        def guardar():
            try:
                id_c = self.db.obtener_o_crear_cliente(en.get(), ea.get(), em.get())
                id_e = next(e['idempleado'] for e in empleados if e['nombre'] == cb_e.get())
                id_s = next(s['idservicio'] for s in servicios if s['nombre'] == cb_s.get())
                fecha_sql = datetime.strptime(f"{ef.get()} {cb_h.get()}:{cb_m.get()}", "%d/%m/%Y %H:%M").strftime("%Y-%m-%d %H:%M:%S")
                
                if self.db.registrar_reserva(id_c, id_e, id_s, fecha_sql):
                    v.destroy()
                    self.cargar_datos()
            except Exception as ex:
                print(f"Error al guardar reserva: {ex}")

        ctk.CTkButton(v, text="CONFIRMAR TURNO", fg_color="#6B8E23", font=("Inter", 14, "bold"), 
                      height=50, width=380, command=guardar).pack(pady=40)

    def abrir_ventana_cobro(self, t):
        # 1. CAMBIO CRÍTICO: Usamos self.master (el tab) en lugar de self
        v = ctk.CTkToplevel(self.master) 
        v.geometry("350x450")
        v.attributes("-topmost", True)
        v.title("Procesar Pago")
        
        db = Database()
        metodos = db.obtener_metodos_pago()
        
        id_reserva = t.get('idreserva')
        precio_base = t.get('Precio_Sugerido', 0)

        ctk.CTkLabel(v, text="FINALIZAR Y COBRAR", font=("Inter", 16, "bold")).pack(pady=20)
        ctk.CTkLabel(v, text=f"Servicio: {t['Servicio']}", font=("Inter", 12)).pack()
        
        ctk.CTkLabel(v, text="Confirmar Monto:", font=("Inter", 12)).pack(pady=(15, 0))
        em = ctk.CTkEntry(v, placeholder_text="Monto", width=200)
        em.insert(0, str(precio_base))
        em.pack(pady=5)
        
        ctk.CTkLabel(v, text="Método de Pago:", font=("Inter", 12)).pack(pady=(10, 0))
        cb = ctk.CTkComboBox(v, values=[m['tipoPago'] for m in metodos], width=200)
        cb.pack(pady=5)

        def conf():
            try:
                monto = em.get()
                id_m = next(m['idmetodopago'] for m in metodos if m['tipoPago'] == cb.get())
                
                if db.finalizar_y_cobrar(id_reserva, monto, id_m):
                    v.destroy()
                    self.cargar_datos() # Esto funciona porque cargar_datos está en esta clase[cite: 14]
                    
                    # 2. CAMBIO DE SEGURIDAD: self.cargar_caja_diaria ya no existe aquí.
                    # Debemos llamar al método del Main (parent) si existe.
                    if hasattr(self.parent, 'cargar_caja_diaria'):
                        self.parent.cargar_caja_diaria()
            except Exception as e:
                print(f"Error al cobrar: {e}")

        ctk.CTkButton(v, text="Confirmar Pago", fg_color="#6B8E23", height=45, command=conf).pack(pady=30)