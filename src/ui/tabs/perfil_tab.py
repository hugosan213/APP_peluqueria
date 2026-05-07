import customtkinter as ctk
from database.connection import Database

class PerfilTab:
    def __init__(self, master, parent):
        self.master = master
        self.parent = parent
        self.db = Database()
        self.setup_ui()

    def setup_ui(self):
        wrapper = ctk.CTkFrame(self.master, fg_color="transparent")
        wrapper.pack(fill="both", expand=True, padx=30, pady=20)

        ctk.CTkLabel(wrapper, text="MI CUENTA", font=("Inter", 24, "bold"), text_color="#5C4033").pack(pady=(0, 10))
        ctk.CTkLabel(wrapper, text="Actualizá tu usuario y contraseña de acceso.", font=("Inter", 12), text_color="#5C4033").pack(pady=(0, 20))

        current_username = self.parent.usuario_actual.get('nombre_usuario', '')
        current_rol = self.parent.usuario_actual.get('rol', '')

        info_frame = ctk.CTkFrame(wrapper, fg_color="#F2F0EB", corner_radius=18, border_width=1, border_color="#E3D6C4")
        info_frame.pack(fill="x", padx=10, pady=(0, 20))

        ctk.CTkLabel(info_frame, text=f"Usuario actual: {current_username}", font=("Inter", 12), text_color="#5C4033").pack(anchor="w", padx=20, pady=(20, 5))
        ctk.CTkLabel(info_frame, text=f"Rol: {current_rol}", font=("Inter", 12), text_color="#5C4033").pack(anchor="w", padx=20, pady=(0, 20))

        self.en_usuario = ctk.CTkEntry(info_frame, placeholder_text="Nuevo usuario", width=420)
        self.en_usuario.pack(pady=(0, 10), padx=20)
        self.en_password = ctk.CTkEntry(info_frame, placeholder_text="Nueva contraseña", width=420, show="*")
        self.en_password.pack(pady=(0, 10), padx=20)
        self.en_password_confirm = ctk.CTkEntry(info_frame, placeholder_text="Confirmar contraseña", width=420, show="*")
        self.en_password_confirm.pack(pady=(0, 20), padx=20)

        self.lbl_feedback = ctk.CTkLabel(info_frame, text="", font=("Inter", 11), text_color="#27632a")
        self.lbl_feedback.pack(pady=(0, 10), padx=20)

        ctk.CTkButton(info_frame, text="Guardar cambios", fg_color="#8B4513", hover_color="#A0522D", corner_radius=12,
                      font=("Inter", 12, "bold"), width=180, command=self.actualizar_credenciales).pack(pady=(0, 20), padx=20)

    def actualizar_credenciales(self):
        nuevo_usuario = self.en_usuario.get().strip()
        nueva_contrasena = self.en_password.get().strip()
        confirmar = self.en_password_confirm.get().strip()

        if not nuevo_usuario and not nueva_contrasena:
            self.lbl_feedback.configure(text="Ingresá un nuevo usuario o nueva contraseña.", text_color="#9D2B2B")
            return

        if nueva_contrasena and nueva_contrasena != confirmar:
            self.lbl_feedback.configure(text="Las contraseñas no coinciden.", text_color="#9D2B2B")
            return

        usuario_actual = self.parent.usuario_actual.get('nombre_usuario', '')
        id_usuario = self.parent.usuario_actual.get('idusuario')

        if nuevo_usuario and nuevo_usuario != usuario_actual:
            if self.db.usuario_existe(nuevo_usuario):
                self.lbl_feedback.configure(text="Ese usuario ya está en uso. Elegí otro.", text_color="#9D2B2B")
                return

        if not nueva_contrasena:
            nueva_contrasena = None

        if not nuevo_usuario:
            nuevo_usuario = usuario_actual

        if self.db.actualizar_credenciales_usuario(id_usuario, nuevo_usuario, nueva_contrasena):
            self.lbl_feedback.configure(text="Credenciales actualizadas correctamente.", text_color="#27632a")
            self.parent.usuario_actual['nombre_usuario'] = nuevo_usuario
            if nueva_contrasena:
                self.parent.usuario_actual['password'] = nueva_contrasena
            self.en_usuario.delete(0, 'end')
            self.en_password.delete(0, 'end')
            self.en_password_confirm.delete(0, 'end')
        else:
            self.lbl_feedback.configure(text="No se pudieron actualizar las credenciales.", text_color="#9D2B2B")
