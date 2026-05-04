import customtkinter as ctk
from database.connection import Database

class ClientesTab:
    def __init__(self, master, parent):
        self.master = master  # El tab físico (este es el que hay que usar para Toplevel)
        self.parent = parent  # La MainWindow
        self.db = Database()
        self.setup_ui()

    def setup_ui(self):
        """Define la interfaz de búsqueda y la lista[cite: 7]"""
        f_busqueda = ctk.CTkFrame(self.master, fg_color="transparent")
        f_busqueda.pack(pady=10, fill="x", padx=20)
        
        self.ent_bus_cli = ctk.CTkEntry(f_busqueda, placeholder_text="Buscar cliente...", width=400)
        self.ent_bus_cli.pack(side="left", padx=10)
        
        ctk.CTkButton(f_busqueda, text="🔍", width=50, fg_color="#C49E6F", hover_color="#E0C085", text_color="black", corner_radius=10,
                      font=("Inter", 12, "bold"), command=self.cargar_lista_clientes).pack(side="left")
        
        self.frame_lista_clientes = ctk.CTkScrollableFrame(self.master, fg_color="transparent")
        self.frame_lista_clientes.pack(fill="both", expand=True, padx=20)
        
        self.cargar_lista_clientes()

    def cargar_lista_clientes(self):
        """Refresca la lista de clientes según la búsqueda[cite: 7]"""
        for widget in self.frame_lista_clientes.winfo_children(): 
            widget.destroy()
            
        busqueda = self.ent_bus_cli.get().lower()
        clientes = self.db.obtener_clientes_lista()

        for c in clientes:
            nombre_completo = f"{c['apellido'] or ''}, {c['nombre'] or ''}"
            
            if busqueda and busqueda not in nombre_completo.lower(): 
                continue

            row = ctk.CTkFrame(self.frame_lista_clientes, fg_color="#FFFFFF", border_width=1, border_color="#E5E1DA", corner_radius=10)
            row.pack(fill="x", pady=3, padx=5)
            
            ctk.CTkLabel(row, text=nombre_completo.upper(), font=("Inter", 13, "bold"), width=250, anchor="w").pack(side="left", padx=20, pady=12)
            
            ctk.CTkButton(row, text="📋 Ver Notas", width=100, fg_color="#8B4513", hover_color="#A0522D", corner_radius=10,
                          font=("Inter", 11, "bold"), command=lambda cli=c: self.abrir_notas_cliente(cli)).pack(side="right", padx=15)

    def abrir_notas_cliente(self, cliente):
        """Abre la ventana de notas corrigiendo el error de referencia"""
        # CAMBIO CLAVE: Usamos self.master en lugar de self
        v = ctk.CTkToplevel(self.master) 
        v.title(f"Historial: {cliente['nombre']}")
        v.geometry("450x550")
        v.attributes("-topmost", True)
        
        ctk.CTkLabel(v, text=f"NOTAS DE {cliente['nombre'].upper()}", font=("Inter", 14, "bold")).pack(pady=15)
        
        txt_notas = ctk.CTkTextbox(v, width=400, height=350)
        txt_notas.pack(pady=10)
        
        if cliente['notas_relevantes']: 
            txt_notas.insert("1.0", cliente['notas_relevantes'])
        
        def guardar():
            if self.db.actualizar_notas_cliente(cliente['idcliente'], txt_notas.get("1.0", "end-1c")):
                v.destroy()
                self.cargar_lista_clientes()
        
        ctk.CTkButton(v, text="Guardar Cambios", fg_color="#8B4513", hover_color="#A0522D", corner_radius=8, command=guardar).pack(pady=20)