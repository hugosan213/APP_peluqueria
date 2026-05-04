import customtkinter as ctk
from database.connection import Database
from tkinter import messagebox

class LoginWindow(ctk.CTk):
    def __init__(self, on_login_success):
        super().__init__()
        self.on_login_success = on_login_success # Función que lanzará la MainWindow
        
        # Configuración de la ventana
        self.title("Acceso al Sistema - Peluquería")
        self.geometry("400x550")
        self.configure(fg_color="#FAF9F6")
        
        # Centrar ventana en pantalla
        self.eval('tk::PlaceWindow . center')

        # Interfaz de Usuario
        self.setup_ui()

    def setup_ui(self):
        # Logo o Título
        ctk.CTkLabel(self, text="BIENVENIDO", font=("Inter", 28, "bold"), text_color="#5C4033").pack(pady=(60, 10))
        ctk.CTkLabel(self, text="Gestión de Peluquería", font=("Inter", 14), text_color="#A67B5B").pack(pady=(0, 40))

        # Campo de Usuario
        self.user_entry = ctk.CTkEntry(self, placeholder_text="Usuario (DNI)", width=280, height=45, corner_radius=10)
        self.user_entry.pack(pady=10)

        # Campo de Contraseña
        self.pass_entry = ctk.CTkEntry(self, placeholder_text="Contraseña", show="*", width=280, height=45, corner_radius=10)
        self.pass_entry.pack(pady=10)

        # Botón de Ingreso
        self.btn_login = ctk.CTkButton(self, text="INICIAR SESIÓN", 
                                        command=self.intentar_login,
                                        width=280, height=52, corner_radius=10,
                                        fg_color="#8B4513", hover_color="#A0522D",
                                        font=("Inter", 14, "bold"))
        self.btn_login.pack(pady=40)

    def intentar_login(self):
        usuario = self.user_entry.get()
        password = self.pass_entry.get()

        if not usuario or not password:
            messagebox.showwarning("Atención", "Por favor, complete todos los campos.")
            return

        db = Database()
        datos_usuario = db.validar_usuario(usuario, password)

        if datos_usuario:
            # SÓLO avisamos del éxito. NO destruimos aquí para evitar el TclError[cite: 5]
            self.on_login_success(datos_usuario) 
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")