import customtkinter as ctk
from database.connection import Database
from datetime import datetime

class MainWindow(ctk.CTk):
    def __init__(self, usuario):
        super().__init__()
        self.usuario_actual = usuario  # Recibimos el objeto con idusuario, nombre_usuario y rol[cite: 8, 13]
        self.title("Peluquería - Gestión Integral")
        self.geometry("1100x850")
        ctk.set_appearance_mode("Light") 
        self.configure(fg_color="#FAF9F6")


        self.tabview = ctk.CTkTabview(self, segmented_button_fg_color="#F2F0EB", 
                                      segmented_button_selected_color="#D2B48C", 
                                      text_color="black")
        self.tabview.pack(pady=10, padx=10, fill="both", expand=True)

        # 1. DEFINICIÓN DE PESTAÑAS SEGÚN ROL[cite: 8, 13]
        self.tab_agenda = self.tabview.add("📅 Agenda")
        self.tab_clientes = self.tabview.add("👥 Clientes")
        self.tab_servicios = self.tabview.add("✂️ Precios")
        self.tab_stock = self.tabview.add("📦 Stock")

        # Solo el administrador ve estas pestañas[cite: 8, 13]
        if self.usuario_actual['rol'] == 'admin':
            self.tab_caja = self.tabview.add("💰 Caja")
            self.tab_gestion = self.tabview.add("⚙️ Config.")
            self.tab_stats = self.tabview.add("📊 Estadísticas")

        # 2. INICIALIZACIÓN DE MÓDULOS
        self.setup_tab_agenda()
        self.setup_tab_clientes()
        self.setup_tab_servicios()
        self.setup_tab_stock()

        if self.usuario_actual['rol'] == 'admin':
            self.setup_tab_caja()
            self.setup_tab_gestion()
            self.setup_tab_stats()
            
        # Este bloque debe ir al final para que quede por encima del Tabview[cite: 14]
        self.btn_logout = ctk.CTkButton(self, text="Cerrar Sesión 🔓", 
                                        fg_color="#CD5C5C", hover_color="#A52A2A",
                                        width=120, height=30, command=self.cerrar_sesion)
        self.btn_logout.place(relx=0.98, rely=0.02, anchor="ne")
        
        self.cargar_datos()

    # --- MÓDULO DE AGENDA ---[cite: 7]
    def setup_tab_agenda(self):
        self.sidebar_agenda = ctk.CTkFrame(self.tab_agenda, width=220, fg_color="#F2F0EB")
        self.sidebar_agenda.pack(side="left", fill="y")
        
        ctk.CTkButton(self.sidebar_agenda, text="➕ Nueva Reserva", fg_color="#6B8E23", command=self.abrir_formulario).pack(pady=20, padx=20, fill="x")
        ctk.CTkButton(self.sidebar_agenda, text="🔄 Actualizar", fg_color="#A67B5B", command=self.cargar_datos).pack(pady=10, padx=20, fill="x")
        
        # Nuevo botón de Historial
        ctk.CTkButton(self.sidebar_agenda, text="📜 Ver Historial", fg_color="#5C4033", command=self.cargar_historial).pack(pady=10, padx=20, fill="x")
        
        self.frame_agenda = ctk.CTkScrollableFrame(self.tab_agenda, fg_color="transparent")
        self.frame_agenda.pack(side="right", fill="both", expand=True, padx=20)

    def cargar_historial(self):
        for widget in self.frame_agenda.winfo_children(): widget.destroy()
        db = Database()
        # Ponemos un título para saber que estamos en el pasado
        ctk.CTkLabel(self.frame_agenda, text="HISTORIAL DE CORTES FINALIZADOS", font=("Inter", 16, "bold")).pack(pady=10)
        
        for t in db.obtener_historial_cortes():
            card = ctk.CTkFrame(self.frame_agenda, fg_color="#E5E1DA", corner_radius=12) # Color grisáceo para diferenciar
            card.pack(fill="x", pady=6, padx=10)
            
            ctk.CTkLabel(card, text=f"🕒 {t['Fecha_Hora']} | 👤 {t['Cliente']}", font=("Inter", 14)).pack(side="left", padx=20, pady=15)
            ctk.CTkLabel(card, text=f"✅ {t['Servicio']}", text_color="#6B8E23", font=("Inter", 12, "italic")).pack(side="right", padx=20)

            
    def cargar_datos(self):
        for widget in self.frame_agenda.winfo_children(): widget.destroy()
        db = Database()
        for t in db.obtener_agenda():
            card = ctk.CTkFrame(self.frame_agenda, fg_color="#FFFFFF", border_width=1, border_color="#E5E1DA", corner_radius=12)
            card.pack(fill="x", pady=6, padx=10)
            ctk.CTkLabel(card, text=f"🕒 {t['Fecha_Hora']} | 👤 {t['Cliente']}", font=("Inter", 14, "bold")).pack(side="left", padx=20, pady=15)
            if t.get('Estado') != 'finalizada':
                ctk.CTkButton(card, text="💵 Cobrar", width=80, fg_color="#6B8E23", command=lambda trn=t: self.abrir_ventana_cobro(trn)).pack(side="right", padx=10)
            ctk.CTkLabel(card, text=f"✂️ {t['Servicio']}", text_color="#5C4033").pack(side="right", padx=20)

    # --- MÓDULO DE CAJA ---[cite: 7]
    def setup_tab_caja(self):
        ctk.CTkLabel(self.tab_caja, text="RESUMEN DE VENTAS DEL DÍA", font=("Inter", 22, "bold"), text_color="#5C4033").pack(pady=30)
        self.frame_caja_info = ctk.CTkFrame(self.tab_caja, fg_color="#F2F0EB", corner_radius=15)
        self.frame_caja_info.pack(pady=10, padx=50, fill="both", expand=True)
        self.cargar_caja_diaria()

    def cargar_caja_diaria(self):
        for widget in self.frame_caja_info.winfo_children(): widget.destroy()
        db = Database()
        resumen = db.obtener_caja_diaria()
        total_general = 0
        if not resumen:
            ctk.CTkLabel(self.frame_caja_info, text="No hay ventas registradas hoy.", font=("Inter", 16)).pack(pady=60)
        else:
            for r in resumen:
                total_general += float(r['total'])
                card = ctk.CTkFrame(self.frame_caja_info, fg_color="#FFFFFF", corner_radius=10)
                card.pack(fill="x", padx=40, pady=10)
                ctk.CTkLabel(card, text=r['tipoPago'].upper(), font=("Inter", 16, "bold")).pack(side="left", padx=20, pady=15)
                ctk.CTkLabel(card, text=f"$ {r['total']}", font=("Inter", 16), text_color="#6B8E23").pack(side="right", padx=20, pady=15)
            ctk.CTkFrame(self.frame_caja_info, height=2, fg_color="#D2B48C").pack(fill="x", padx=30, pady=20)
            ctk.CTkLabel(self.frame_caja_info, text=f"TOTAL ACUMULADO: $ {total_general}", font=("Inter", 24, "bold")).pack(pady=10)

    # --- MÓDULO DE STOCK ---[cite: 7]
    def setup_tab_stock(self):
        f_top = ctk.CTkFrame(self.tab_stock, fg_color="transparent"); f_top.pack(pady=10, fill="x", padx=30)
        ctk.CTkLabel(f_top, text="CONTROL DE INSUMOS", font=("Inter", 20, "bold")).pack(side="left")
        ctk.CTkButton(f_top, text="+ Nuevo Producto", fg_color="#6B8E23", command=self.abrir_formulario_producto).pack(side="right")
        self.frame_lista_stock = ctk.CTkScrollableFrame(self.tab_stock, fg_color="transparent")
        self.frame_lista_stock.pack(fill="both", expand=True, padx=30); self.cargar_lista_stock()

    def cargar_lista_stock(self):
        for widget in self.frame_lista_stock.winfo_children(): widget.destroy()
        db = Database()
        for p in db.obtener_productos_stock():
            es_bajo = p['stock_actual'] <= p['stock_minimo']
            row = ctk.CTkFrame(self.frame_lista_stock, fg_color="#FFCDD2" if es_bajo else "#FFFFFF", border_width=1, border_color="#E5E1DA", corner_radius=10)
            row.pack(fill="x", pady=5, padx=5)
            ctk.CTkLabel(row, text=p['nombre'].upper(), font=("Inter", 13, "bold"), width=250, anchor="w").pack(side="left", padx=20, pady=10)
            ctk.CTkLabel(row, text=f"Stock: {p['stock_actual']} {p['unidad']}").pack(side="left", padx=20)

    def abrir_formulario_producto(self):
        v = ctk.CTkToplevel(self); v.geometry("400x500"); v.attributes("-topmost", True)
        ctk.CTkLabel(v, text="NUEVO PRODUCTO", font=("Inter", 16, "bold")).pack(pady=20)
        en = ctk.CTkEntry(v, placeholder_text="Nombre", width=300); en.pack(pady=10)
        es = ctk.CTkEntry(v, placeholder_text="Stock Actual", width=300); es.pack(pady=10)
        em = ctk.CTkEntry(v, placeholder_text="Stock Mínimo", width=300); em.pack(pady=10)
        eu = ctk.CTkEntry(v, placeholder_text="Unidad", width=300); eu.pack(pady=10)
        def add():
            if Database().agregar_producto_stock(en.get(), es.get(), em.get(), eu.get()):
                v.destroy(); self.cargar_lista_stock()
        ctk.CTkButton(v, text="Guardar", fg_color="#6B8E23", command=add).pack(pady=30)

    # --- MÓDULO DE SERVICIOS ---[cite: 7]
   # --- MÓDULO DE PRECIOS Y SERVICIOS ---
    def setup_tab_servicios(self):
        f_top = ctk.CTkFrame(self.tab_servicios, fg_color="transparent")
        f_top.pack(pady=10, fill="x", padx=30)
        
        ctk.CTkLabel(f_top, text="GESTIÓN DE TARIFAS", font=("Inter", 20, "bold"), text_color="#5C4033").pack(side="left")
        ctk.CTkButton(f_top, text="+ Nuevo Servicio", fg_color="#6B8E23", command=self.abrir_formulario_servicio).pack(side="right")
        
        self.frame_lista_precios = ctk.CTkScrollableFrame(self.tab_servicios, fg_color="transparent")
        self.frame_lista_precios.pack(fill="both", expand=True, padx=30)
        self.cargar_servicios_edicion()

    def cargar_servicios_edicion(self):
        # Limpiamos la lista antes de recargar
        for widget in self.frame_lista_precios.winfo_children(): 
            widget.destroy()
            
        db = Database()
        for s in db.obtener_servicios_detallados():
            row = ctk.CTkFrame(self.frame_lista_precios, fg_color="#FFFFFF", border_width=1, border_color="#E5E1DA", corner_radius=10)
            row.pack(fill="x", pady=4, padx=5)
            
            # Nombre del servicio
            ctk.CTkLabel(row, text=s['nombre'].upper(), width=200, anchor="w", font=("Inter", 12, "bold")).pack(side="left", padx=20, pady=10)
            
            # Entradas para precio y duración[cite: 7]
            ctk.CTkLabel(row, text="$").pack(side="left")
            e_p = ctk.CTkEntry(row, width=80)
            e_p.insert(0, str(s['precio']))
            e_p.pack(side="left", padx=5)
            
            ctk.CTkLabel(row, text="Min:").pack(side="left", padx=(10,0))
            e_d = ctk.CTkEntry(row, width=60)
            e_d.insert(0, str(s['duracion']))
            e_d.pack(side="left", padx=5)
            
            # Botones de acción[cite: 7]
            ctk.CTkButton(row, text="💾", width=40, fg_color="#6B8E23", 
                          command=lambda i=s['idservicio'], p=e_p, d=e_d: self.guardar_cambio_servicio(i, p.get(), d.get())).pack(side="right", padx=5)
            
            ctk.CTkButton(row, text="🗑️", width=40, fg_color="#CD5C5C", 
                          command=lambda i=s['idservicio']: self.borrar_servicio(i)).pack(side="right", padx=5)

    def guardar_cambio_servicio(self, id_s, p, d):
        if Database().actualizar_servicio(id_s, p, d):
            self.cargar_servicios_edicion()

    def borrar_servicio(self, id_s):
        if Database().eliminar_servicio(id_s):
            self.cargar_servicios_edicion()

    def abrir_formulario_servicio(self):
        v = ctk.CTkToplevel(self); v.geometry("300x400"); v.attributes("-topmost", True)
        en = ctk.CTkEntry(v, placeholder_text="Nombre"); en.pack(pady=10)
        ep = ctk.CTkEntry(v, placeholder_text="Precio"); ep.pack(pady=10)
        ed = ctk.CTkEntry(v, placeholder_text="Minutos"); ed.pack(pady=10)
        def add():
            if Database().agregar_servicio_nuevo(en.get(), ep.get(), ed.get()):
                v.destroy(); self.cargar_servicios_edicion()
        ctk.CTkButton(v, text="Guardar", fg_color="#6B8E23", command=add).pack(pady=20)

   # --- MÓDULO DE CLIENTES (RESTRICTO Y FUNCIONAL) ---
    def setup_tab_clientes(self):
        # Contenedor para la barra de búsqueda
        f_busqueda = ctk.CTkFrame(self.tab_clientes, fg_color="transparent")
        f_busqueda.pack(pady=10, fill="x", padx=20)
        
        self.ent_bus_cli = ctk.CTkEntry(f_busqueda, placeholder_text="Buscar cliente por nombre o apellido...", width=400)
        self.ent_bus_cli.pack(side="left", padx=10)
        
        # Botón de lupa para ejecutar la búsqueda
        ctk.CTkButton(f_busqueda, text="🔍", width=50, fg_color="#D2B48C", text_color="black", 
                      command=self.cargar_lista_clientes).pack(side="left")
        
        # Frame scrolleable para la lista[cite: 7]
        self.frame_lista_clientes = ctk.CTkScrollableFrame(self.tab_clientes, fg_color="transparent")
        self.frame_lista_clientes.pack(fill="both", expand=True, padx=20)
        
        self.cargar_lista_clientes()

    def cargar_lista_clientes(self):
        # Limpiamos la lista actual[cite: 7]
        for widget in self.frame_lista_clientes.winfo_children(): 
            widget.destroy()
            
        db = Database()
        busqueda = self.ent_bus_cli.get().lower()
        clientes = db.obtener_clientes_lista()

        for c in clientes:
            nombre_completo = f"{c['apellido'] or ''}, {c['nombre'] or ''}"
            
            # Filtro dinámico[cite: 7]
            if busqueda and busqueda not in nombre_completo.lower(): 
                continue

            # Tarjeta visual del cliente[cite: 7]
            row = ctk.CTkFrame(self.frame_lista_clientes, fg_color="#FFFFFF", border_width=1, border_color="#E5E1DA", corner_radius=10)
            row.pack(fill="x", pady=3, padx=5)
            
            ctk.CTkLabel(row, text=nombre_completo.upper(), font=("Inter", 13, "bold"), width=250, anchor="w").pack(side="left", padx=20, pady=12)
            
            # Botón para abrir el historial/notas[cite: 7]
            ctk.CTkButton(row, text="📋 Ver Notas", width=100, fg_color="#A67B5B", 
                          command=lambda cli=c: self.abrir_notas_cliente(cli)).pack(side="right", padx=15)

    def abrir_notas_cliente(self, cliente):
        v = ctk.CTkToplevel(self)
        v.title(f"Historial: {cliente['nombre']}")
        v.geometry("450x550")
        v.attributes("-topmost", True)
        
        ctk.CTkLabel(v, text=f"NOTAS DE {cliente['nombre'].upper()}", font=("Inter", 14, "bold")).pack(pady=15)
        
        txt_notas = ctk.CTkTextbox(v, width=400, height=350)
        txt_notas.pack(pady=10)
        
        # Cargar notas existentes si las hay[cite: 7]
        if cliente['notas_relevantes']: 
            txt_notas.insert("1.0", cliente['notas_relevantes'])
        
        def guardar():
            db = Database()
            if db.actualizar_notas_cliente(cliente['idcliente'], txt_notas.get("1.0", "end-1c")):
                v.destroy()
                self.cargar_lista_clientes()
        
        ctk.CTkButton(v, text="Guardar Cambios", fg_color="#6B8E23", command=guardar).pack(pady=20)

    # --- CONFIGURACIÓN ---[cite: 7, 8]
    def setup_tab_gestion(self):
        container = ctk.CTkFrame(self.tab_gestion, fg_color="#F2F0EB", corner_radius=15)
        container.pack(pady=50, padx=50, expand=True)
        ctk.CTkLabel(container, text="REGISTRAR NUEVO EMPLEADO", font=("Inter", 20, "bold")).pack(pady=20)
        self.en_nom = ctk.CTkEntry(container, placeholder_text="Nombre", width=400); self.en_nom.pack(pady=5)
        self.en_ape = ctk.CTkEntry(container, placeholder_text="Apellido", width=400); self.en_ape.pack(pady=5)
        self.en_dni = ctk.CTkEntry(container, placeholder_text="DNI", width=400); self.en_dni.pack(pady=5)
        self.en_mai = ctk.CTkEntry(container, placeholder_text="Email", width=400); self.en_mai.pack(pady=5)
        ctk.CTkButton(container, text="Registrar Peluquero/a", fg_color="#5C4033", command=self.guardar_empleado).pack(pady=20)

    def guardar_empleado(self):
        db = Database()
        if db.agregar_empleado(self.en_nom.get(), self.en_ape.get(), self.en_mai.get(), self.en_dni.get()):
            for e in [self.en_nom, self.en_ape, self.en_dni, self.en_mai]: e.delete(0, 'end')

    def abrir_formulario(self):
        v = ctk.CTkToplevel(self)
        v.title("NUEVA RESERVA")
        v.geometry("500x750")
        v.attributes("-topmost", True)
        v.configure(fg_color="#FAF9F6")

        db = Database()
        # Traemos los datos actuales de la BD para llenar los selectores[cite: 7]
        empleados = db.obtener_empleados()
        servicios = db.obtener_servicios()

        # --- SECCIÓN CLIENTE ---
        ctk.CTkLabel(v, text="DATOS DEL CLIENTE", font=("Inter", 16, "bold"), text_color="#5C4033").pack(pady=(20, 10))
        en = ctk.CTkEntry(v, placeholder_text="Nombre", width=380); en.pack(pady=5)
        ea = ctk.CTkEntry(v, placeholder_text="Apellido", width=380); ea.pack(pady=5)
        em = ctk.CTkEntry(v, placeholder_text="Email (Opcional)", width=380); em.pack(pady=5)

        # --- SECCIÓN TURNO ---
        ctk.CTkLabel(v, text="DETALLES DEL TURNO", font=("Inter", 16, "bold"), text_color="#5C4033").pack(pady=(30, 10))
        
        ctk.CTkLabel(v, text="Seleccionar Peluquero/a:").pack()
        cb_e = ctk.CTkComboBox(v, values=[e['nombre'] for e in empleados], width=380)
        cb_e.pack(pady=5)

        ctk.CTkLabel(v, text="Seleccionar Servicio:").pack()
        cb_s = ctk.CTkComboBox(v, values=[s['nombre'] for s in servicios], width=380)
        cb_s.pack(pady=5)

        # --- FECHA Y HORA ---
        ctk.CTkLabel(v, text="Fecha (DD/MM/YYYY):").pack(pady=(15, 0))
        ef = ctk.CTkEntry(v, width=380)
        ef.insert(0, datetime.now().strftime("%d/%m/%Y")) # Fecha de hoy por defecto[cite: 7]
        ef.pack(pady=5)

        ctk.CTkLabel(v, text="Seleccionar Horario:").pack(pady=(10, 0))
        f_h = ctk.CTkFrame(v, fg_color="transparent")
        f_h.pack(pady=5)
        
        cb_h = ctk.CTkComboBox(f_h, values=[f"{i:02d}" for i in range(8, 21)], width=80)
        cb_h.set("10"); cb_h.pack(side="left", padx=5)
        
        ctk.CTkLabel(f_h, text=":").pack(side="left")
        
        cb_m = ctk.CTkComboBox(f_h, values=["00", "15", "30", "45"], width=80)
        cb_m.set("00"); cb_m.pack(side="left", padx=5)

        def guardar():
            try:
                # 1. Obtenemos o creamos el cliente en la BD[cite: 7]
                id_c = db.obtener_o_crear_cliente(en.get(), ea.get(), em.get() or "temp@mail.com")
                
                # 2. Mappeamos los IDs de lo seleccionado en los ComboBox[cite: 7]
                id_e = next(e['idempleado'] for e in empleados if e['nombre'] == cb_e.get())
                id_s = next(s['idservicio'] for s in servicios if s['nombre'] == cb_s.get())
                
                # 3. Formateamos la fecha completa para MySQL[cite: 7]
                fecha_sql = datetime.strptime(f"{ef.get()} {cb_h.get()}:{cb_m.get()}", "%d/%m/%Y %H:%M").strftime("%Y-%m-%d %H:%M:%S")
                
                if db.registrar_reserva(id_c, id_e, id_s, fecha_sql):
                    v.destroy()
                    self.cargar_datos() # Refrescamos la agenda principal[cite: 7]
            except Exception as ex:
                print(f"Error al guardar reserva: {ex}")

        ctk.CTkButton(v, text="CONFIRMAR TURNO", fg_color="#6B8E23", hover_color="#556B2F",
                      font=("Inter", 14, "bold"), height=50, width=380, command=guardar).pack(pady=40)

    def abrir_ventana_cobro(self, t):
        v = ctk.CTkToplevel(self)
        v.geometry("350x450")
        v.attributes("-topmost", True)
        v.title("Procesar Pago")
        
        db = Database()
        metodos = db.obtener_metodos_pago()
        
        id_reserva = t.get('idreserva')
        precio_base = t.get('Precio_Sugerido', 0) # Traemos el precio de la reserva

        ctk.CTkLabel(v, text="FINALIZAR Y COBRAR", font=("Inter", 16, "bold")).pack(pady=20)
        
        ctk.CTkLabel(v, text=f"Servicio: {t['Servicio']}", font=("Inter", 12)).pack()
        
        ctk.CTkLabel(v, text="Confirmar Monto:", font=("Inter", 12)).pack(pady=(15, 0))
        em = ctk.CTkEntry(v, placeholder_text="Monto", width=200)
        em.insert(0, str(precio_base)) # ¡Acá sucede la magia! Ya aparece el precio
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
                    self.cargar_datos()
                    self.cargar_caja_diaria()
            except Exception as e:
                print(f"Error al cobrar: {e}")

        ctk.CTkButton(v, text="Confirmar Pago", fg_color="#6B8E23", height=45, command=conf).pack(pady=30)
    def setup_tab_caja(self):
        # Limpiamos lo que haya
        for widget in self.tab_caja.winfo_children(): widget.destroy()
        
        f_top = ctk.CTkFrame(self.tab_caja, fg_color="transparent")
        f_top.pack(pady=20, fill="x", padx=50)
        
        ctk.CTkLabel(f_top, text="CONTROL DE CAJA DIARIA", font=("Inter", 22, "bold")).pack(side="left")
        ctk.CTkButton(f_top, text="- Retirar Dinero / Gasto", fg_color="#CD5C5C", command=self.abrir_formulario_egreso).pack(side="right")
        
        self.frame_caja_info = ctk.CTkFrame(self.tab_caja, fg_color="#F2F0EB", corner_radius=15)
        self.frame_caja_info.pack(pady=10, padx=50, fill="both", expand=True)
        self.cargar_caja_diaria()

    def cargar_caja_diaria(self):
        for widget in self.frame_caja_info.winfo_children(): widget.destroy()
        db = Database()
        ingresos = db.obtener_caja_diaria()
        egresos_total = db.obtener_total_egresos_hoy()
        total_ingresos = sum(float(r['total']) for r in ingresos)
        
        # Mostrar Ingresos
        ctk.CTkLabel(self.frame_caja_info, text="INGRESOS", font=("Inter", 14, "bold")).pack(pady=(10,5))
        for r in ingresos:
            card = ctk.CTkFrame(self.frame_caja_info, fg_color="#FFFFFF"); card.pack(fill="x", padx=40, pady=2)
            ctk.CTkLabel(card, text=f"{r['tipoPago']}: $ {r['total']}").pack(pady=5)

        # Mostrar Egresos
        ctk.CTkFrame(self.frame_caja_info, height=2, fg_color="#D2B48C").pack(fill="x", padx=30, pady=15)
        ctk.CTkLabel(self.frame_caja_info, text=f"TOTAL EGRESOS: - $ {egresos_total}", text_color="#CD5C5C", font=("Inter", 16, "bold")).pack()

        # Saldo Final
        saldo_neto = total_ingresos - float(egresos_total)
        ctk.CTkLabel(self.frame_caja_info, text=f"SALDO EN CAJA: $ {saldo_neto}", 
                     font=("Inter", 26, "bold"), text_color="#2D2424").pack(pady=20)

    def abrir_formulario_egreso(self):
        # 1. Pedimos la contraseña antes de abrir cualquier ventana
        dialogo = ctk.CTkInputDialog(text="Ingrese su contraseña para autorizar el retiro:", title="Seguridad de Caja")
        # El método get_input() detiene la ejecución hasta que el usuario responde[cite: 7]
        password_ingresada = dialogo.get_input()

        # 2. Verificamos la contraseña ingresada contra la del usuario logueado[cite: 8, 10]
        # Usamos self.usuario_actual['password'] porque ese dato ya lo traemos desde la DB[cite: 8]
        if password_ingresada == self.usuario_actual.get('password'):
            v = ctk.CTkToplevel(self)
            v.geometry("350x400")
            v.attributes("-topmost", True)
            v.title("Nuevo Egreso")
            
            ctk.CTkLabel(v, text="SALIDA DE DINERO", font=("Inter", 16, "bold")).pack(pady=20)
            
            em = ctk.CTkEntry(v, placeholder_text="Monto", width=250)
            em.pack(pady=10)
            
            ed = ctk.CTkEntry(v, placeholder_text="Descripción", width=250)
            ed.pack(pady=10)
            
            def guardar():
                monto = em.get()
                desc = ed.get()
                if not monto or not desc:
                    from tkinter import messagebox
                    messagebox.showwarning("Atención", "Complete todos los campos.")
                    return
                
                if Database().registrar_egreso(monto, desc):
                    v.destroy()
                    self.cargar_caja_diaria() # Refrescamos los totales en la pestaña[cite: 7]
            
            ctk.CTkButton(v, text="Confirmar Gasto", fg_color="#CD5C5C", command=guardar).pack(pady=30)
            
        elif password_ingresada is not None:
            # Si la contraseña es incorrecta y no se presionó "Cancelar"[cite: 7]
            from tkinter import messagebox
            messagebox.showerror("Error", "Contraseña incorrecta. Operación cancelada.")

    def setup_tab_stats(self):
        # Título y Botón de Exportar
        f_top = ctk.CTkFrame(self.tab_stats, fg_color="transparent")
        f_top.pack(pady=20, fill="x", padx=50)
        
        ctk.CTkLabel(f_top, text="REPORTES DE INGRESOS", font=("Inter", 22, "bold")).pack(side="left")
        
        # Botón para imprimir el Excel/CSV
        ctk.CTkButton(f_top, text="📊 Exportar Excel (CSV)", fg_color="#5C4033", 
                      command=self.exportar_estadisticas_excel).pack(side="right", padx=10)
        
        self.selector_periodo = ctk.CTkComboBox(f_top, values=["Semanal", "Mensual", "Anual"], 
                                                command=lambda _: self.actualizar_grafico())
        self.selector_periodo.set("Mensual")
        self.selector_periodo.pack(side="right")

        # Contenedor para los resultados visuales
        self.frame_grafico = ctk.CTkFrame(self.tab_stats, fg_color="#F2F0EB", corner_radius=15)
        self.frame_grafico.pack(pady=10, padx=50, fill="both", expand=True)
        self.actualizar_grafico()
    def actualizar_grafico(self):
        for widget in self.frame_grafico.winfo_children(): widget.destroy()
        
        periodo = self.selector_periodo.get()
        datos = Database().obtener_estadisticas_ingresos(periodo)

        if not datos:
            ctk.CTkLabel(self.frame_grafico, text=f"No hay datos suficientes para el reporte {periodo.lower()}.").pack(pady=100)
            return

        # Generamos barritas visuales simples[cite: 5]
        max_valor = max(float(d['total']) for d in datos) if datos else 1
        
        for d in datos:
            row = ctk.CTkFrame(self.frame_grafico, fg_color="transparent")
            row.pack(fill="x", padx=30, pady=10)
            
            ctk.CTkLabel(row, text=str(d['etiqueta']).upper(), width=100, anchor="w").pack(side="left")
            
            # Calculamos el ancho de la barra proporcional al total[cite: 5]
            ancho_barra = (float(d['total']) / max_valor) * 400
            ctk.CTkFrame(row, width=ancho_barra, height=20, fg_color="#D2B48C", corner_radius=5).pack(side="left", padx=10)
            
            ctk.CTkLabel(row, text=f"$ {d['total']}", font=("Inter", 12, "bold")).pack(side="left")

    
    
    def setup_tab_servicios(self):
        f_top = ctk.CTkFrame(self.tab_servicios, fg_color="transparent")
        f_top.pack(pady=10, fill="x", padx=30)
        ctk.CTkLabel(f_top, text="GESTIÓN DE TARIFAS", font=("Inter", 20, "bold"), text_color="#5C4033").pack(side="left")
        
        # Seguridad: Solo el admin puede agregar servicios nuevos[cite: 13]
        if self.usuario_actual['rol'] == 'admin':
            ctk.CTkButton(f_top, text="+ Nuevo Servicio", fg_color="#6B8E23", command=self.abrir_formulario_servicio).pack(side="right")
        
        self.frame_lista_precios = ctk.CTkScrollableFrame(self.tab_servicios, fg_color="transparent")
        self.frame_lista_precios.pack(fill="both", expand=True, padx=30)
        self.cargar_servicios_edicion()

    def cargar_servicios_edicion(self):
        for widget in self.frame_lista_precios.winfo_children(): 
            widget.destroy()
            
        db = Database()
        es_admin = self.usuario_actual['rol'] == 'admin'

        for s in db.obtener_servicios_detallados():
            row = ctk.CTkFrame(self.frame_lista_precios, fg_color="#FFFFFF", border_width=1, border_color="#E5E1DA", corner_radius=10)
            row.pack(fill="x", pady=4, padx=5)
            
            ctk.CTkLabel(row, text=s['nombre'].upper(), width=200, anchor="w", font=("Inter", 12, "bold")).pack(side="left", padx=20, pady=10)
            
            ctk.CTkLabel(row, text="$").pack(side="left")
            e_p = ctk.CTkEntry(row, width=80)
            e_p.insert(0, str(s['precio']))
            # Si es empleado, solo lectura[cite: 13]
            if not es_admin: e_p.configure(state="disabled")
            e_p.pack(side="left", padx=5)
            
            ctk.CTkLabel(row, text="Min:").pack(side="left", padx=(10,0))
            e_d = ctk.CTkEntry(row, width=60)
            e_d.insert(0, str(s['duracion']))
            if not es_admin: e_d.configure(state="disabled")
            e_d.pack(side="left", padx=5)
            
            # Botones de acción: Visibles solo para el administrador[cite: 13]
            if es_admin:
                ctk.CTkButton(row, text="💾", width=40, fg_color="#6B8E23", 
                              command=lambda i=s['idservicio'], p=e_p, d=e_d: self.guardar_cambio_servicio(i, p.get(), d.get())).pack(side="right", padx=5)
                ctk.CTkButton(row, text="🗑️", width=40, fg_color="#CD5C5C", 
                              command=lambda i=s['idservicio']: self.borrar_servicio(i)).pack(side="right", padx=5)

    def setup_tab_stock(self):
            f_top = ctk.CTkFrame(self.tab_stock, fg_color="transparent")
            f_top.pack(pady=10, fill="x", padx=30)
            ctk.CTkLabel(f_top, text="CONTROL DE INSUMOS", font=("Inter", 20, "bold")).pack(side="left")
            
            # BLOQUEO SEGURIDAD: Solo admin crea productos[cite: 4]
            if self.usuario_actual['rol'] == 'admin':
                ctk.CTkButton(f_top, text="+ Nuevo Producto", fg_color="#6B8E23", command=self.abrir_formulario_producto).pack(side="right")
                
            self.frame_lista_stock = ctk.CTkScrollableFrame(self.tab_stock, fg_color="transparent")
            self.frame_lista_stock.pack(fill="both", expand=True, padx=30)
            self.cargar_lista_stock()

    def cerrar_sesion(self):
        from tkinter import messagebox
        if messagebox.askyesno("Cerrar Sesión", "¿Estás seguro que querés salir?"):
            # 1. Obtenemos la referencia a la ventana de login antes de destruir esta
            from ui.login import LoginWindow
            
            # 2. Cerramos la ventana principal y detenemos su loop
            self.quit()
            self.destroy()
            
            # 3. Lanzamos el login como una tarea nueva para evitar el KeyboardInterrupt
            def reiniciar():
                def relog(usuario):
                    from ui.main_window import MainWindow
                    app = MainWindow(usuario)
                    app.mainloop()
                
                nuevo_login = LoginWindow(on_login_success=relog)
                nuevo_login.mainloop()
            
            reiniciar()

    def exportar_estadisticas_excel(self):
        from tkinter import filedialog, messagebox
        import pandas as pd
        
        db = Database()
        datos = db.obtener_pagos_para_exportar()
        
        if not datos:
            messagebox.showinfo("Exportar", "No hay datos de ventas para exportar.")
            return
            
        path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel Workbook", "*.xlsx")],
            initialfile=f"Reporte_Ventas_{datetime.now().strftime('%d_%m_%Y')}.xlsx"
        )
        
        if path:
            try:
                # 1. Creamos el DataFrame
                df = pd.DataFrame(datos)
                df.columns = ['ID Pago', 'Fecha y Hora', 'Monto ($)', 'Método de Pago', 'Servicio']
                
                # 2. Usamos un "ExcelWriter" para poder aplicar formatos
                with pd.ExcelWriter(path, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='Ventas')
                    
                    # 3. Auto-ajuste de columnas automático
                    worksheet = writer.sheets['Ventas']
                    for idx, col in enumerate(df.columns):
                        # Encontramos el largo máximo del contenido en esa columna
                        max_len = max(
                            df[col].astype(str).map(len).max(),
                            len(col)
                        ) + 2 # Margen extra
                        worksheet.column_dimensions[chr(65 + idx)].width = max_len
                
                messagebox.showinfo("Éxito", f"Reporte profesional generado en:\n{path}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo generar el Excel: {e}")
