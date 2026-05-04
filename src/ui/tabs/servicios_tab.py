import customtkinter as ctk
from database.connection import Database

class ServiciosTab:
    def __init__(self, master, parent):
        self.master = master
        self.parent = parent
        self.db = Database()
        self.setup_ui()

    def setup_ui(self):
        f_top = ctk.CTkFrame(self.master, fg_color="transparent")
        f_top.pack(pady=10, fill="x", padx=30)
        
        ctk.CTkLabel(f_top, text="GESTIÓN DE TARIFAS", font=("Inter", 20, "bold"), text_color="#5C4033").pack(side="left")
        
        # Corrección: Acceso al rol a través de self.parent[cite: 18]
        if self.parent.usuario_actual['rol'] == 'admin':
            ctk.CTkButton(f_top, text="+ Nuevo Servicio", fg_color="#6B8E23", command=self.abrir_formulario_servicio).pack(side="right")
        
        self.frame_lista_precios = ctk.CTkScrollableFrame(self.master, fg_color="transparent")
        self.frame_lista_precios.pack(fill="both", expand=True, padx=30)
        self.cargar_servicios_edicion()

    def cargar_servicios_edicion(self):
        for widget in self.frame_lista_precios.winfo_children(): 
            widget.destroy()
            
        # Corrección: Acceso al rol a través de self.parent[cite: 18]
        es_admin = self.parent.usuario_actual['rol'] == 'admin'

        for s in self.db.obtener_servicios_detallados():
            row = ctk.CTkFrame(self.frame_lista_precios, fg_color="#FFFFFF", border_width=1, border_color="#E5E1DA", corner_radius=10)
            row.pack(fill="x", pady=4, padx=5)
            
            ctk.CTkLabel(row, text=s['nombre'].upper(), width=200, anchor="w", font=("Inter", 12, "bold")).pack(side="left", padx=20, pady=10)
            
            ctk.CTkLabel(row, text="$").pack(side="left")
            e_p = ctk.CTkEntry(row, width=80)
            e_p.insert(0, str(s['precio']))
            if not es_admin: e_p.configure(state="disabled")
            e_p.pack(side="left", padx=5)
            
            ctk.CTkLabel(row, text="Min:").pack(side="left", padx=(10,0))
            e_d = ctk.CTkEntry(row, width=60)
            e_d.insert(0, str(s['duracion']))
            if not es_admin: e_d.configure(state="disabled")
            e_d.pack(side="left", padx=5)
            
            if es_admin:
                ctk.CTkButton(row, text="💾", width=40, fg_color="#6B8E23", 
                              command=lambda i=s['idservicio'], p=e_p, d=e_d: self.guardar_cambio_servicio(i, p.get(), d.get())).pack(side="right", padx=5)
                ctk.CTkButton(row, text="🗑️", width=40, fg_color="#CD5C5C", 
                              command=lambda i=s['idservicio']: self.borrar_servicio(i)).pack(side="right", padx=5)

    def guardar_cambio_servicio(self, id_s, p, d):
        if self.db.actualizar_servicio(id_s, p, d):
            self.cargar_servicios_edicion()

    def borrar_servicio(self, id_s):
        if self.db.eliminar_servicio(id_s):
            self.cargar_servicios_edicion()

    def abrir_formulario_servicio(self):
        # Corrección: Usar self.master para evitar error de Tkinter[cite: 17]
        v = ctk.CTkToplevel(self.master)
        v.geometry("300x400")
        v.attributes("-topmost", True)
        en = ctk.CTkEntry(v, placeholder_text="Nombre"); en.pack(pady=10)
        ep = ctk.CTkEntry(v, placeholder_text="Precio"); ep.pack(pady=10)
        ed = ctk.CTkEntry(v, placeholder_text="Minutos"); ed.pack(pady=10)
        def add():
            if self.db.agregar_servicio_nuevo(en.get(), ep.get(), ed.get()):
                v.destroy()
                self.cargar_servicios_edicion()
        ctk.CTkButton(v, text="Guardar", fg_color="#6B8E23", command=add).pack(pady=20)