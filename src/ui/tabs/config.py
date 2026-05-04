import customtkinter as ctk
from database.connection import Database

class ConfigTab:
    def __init__(self, master, main_window):
        self.master = master
        self.main_window = main_window
        self.setup_tab_gestion()

    def setup_tab_gestion(self):
        container = ctk.CTkFrame(self.master, fg_color="#F2F0EB", corner_radius=15)
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