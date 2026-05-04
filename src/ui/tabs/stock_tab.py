import customtkinter as ctk
from database.connection import Database

class StockTab:
    def __init__(self, master, parent):
        self.master = master  # El tab físico
        self.parent = parent  # MainWindow
        self.db = Database()
        self.setup_ui()

    def setup_ui(self):
        """Estructura de control de insumos[cite: 7]"""
        f_top = ctk.CTkFrame(self.master, fg_color="transparent")
        f_top.pack(pady=10, fill="x", padx=30)
        
        ctk.CTkLabel(f_top, text="CONTROL DE INSUMOS", font=("Inter", 20, "bold")).pack(side="left")
        
        # Seguridad: Solo admin crea productos[cite: 13, 15]
        if self.parent.usuario_actual['rol'] == 'admin':
            ctk.CTkButton(f_top, text="+ Nuevo Producto", fg_color="#6B8E23", 
                          command=self.abrir_formulario_producto).pack(side="right")
            
        self.frame_lista_stock = ctk.CTkScrollableFrame(self.master, fg_color="transparent")
        self.frame_lista_stock.pack(fill="both", expand=True, padx=30)
        self.cargar_lista_stock()

    def cargar_lista_stock(self):
        """Refresca la lista de productos y marca en rojo los que tienen stock bajo[cite: 7]"""
        for widget in self.frame_lista_stock.winfo_children(): 
            widget.destroy()
            
        # Usamos la conexión self.db ya inicializada
        for p in self.db.obtener_productos_stock():
            es_bajo = p['stock_actual'] <= p['stock_minimo']
            row = ctk.CTkFrame(self.frame_lista_stock, 
                               fg_color="#FFCDD2" if es_bajo else "#FFFFFF", 
                               border_width=1, border_color="#E5E1DA", corner_radius=10)
            row.pack(fill="x", pady=5, padx=5)
            
            ctk.CTkLabel(row, text=p['nombre'].upper(), font=("Inter", 13, "bold"), width=250, anchor="w").pack(side="left", padx=20, pady=10)
            ctk.CTkLabel(row, text=f"Stock: {p['stock_actual']} {p['unidad']}").pack(side="left", padx=20)

    def abrir_formulario_producto(self):
        """Ventana para agregar un nuevo insumo[cite: 7]"""
        # CORRECCIÓN: Usamos self.master para evitar el error de Tkinter
        v = ctk.CTkToplevel(self.master)
        v.geometry("400x500")
        v.attributes("-topmost", True)
        v.title("Nuevo Producto")

        ctk.CTkLabel(v, text="NUEVO PRODUCTO", font=("Inter", 16, "bold")).pack(pady=20)
        en = ctk.CTkEntry(v, placeholder_text="Nombre", width=300); en.pack(pady=10)
        es = ctk.CTkEntry(v, placeholder_text="Stock Actual", width=300); es.pack(pady=10)
        em = ctk.CTkEntry(v, placeholder_text="Stock Mínimo", width=300); em.pack(pady=10)
        eu = ctk.CTkEntry(v, placeholder_text="Unidad", width=300); eu.pack(pady=10)

        def add():
            # Usamos self.db para la inserción[cite: 17]
            if self.db.agregar_producto_stock(en.get(), es.get(), em.get(), eu.get()):
                v.destroy()
                self.cargar_lista_stock()

        ctk.CTkButton(v, text="Guardar", fg_color="#6B8E23", command=add).pack(pady=30)