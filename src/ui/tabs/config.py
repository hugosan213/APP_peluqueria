import customtkinter as ctk
from database.connection import Database

class ConfigTab:
    def __init__(self, master, main_window):
        self.master = master
        self.main_window = main_window
        self.db = Database()
        self.setup_tab_gestion()

    def setup_tab_gestion(self):
        wrapper = ctk.CTkFrame(self.master, fg_color="transparent")
        wrapper.pack(fill="both", expand=True, padx=30, pady=20)

        ctk.CTkLabel(wrapper, text="REGISTRAR NUEVO EMPLEADO", font=("Inter", 22, "bold"), text_color="#5C4033").pack(pady=(0, 10))
        ctk.CTkLabel(wrapper, text="Completa los datos y registra al empleado para usarlo en agenda y cobros.", font=("Inter", 12), text_color="#5C4033").pack(pady=(0, 20))

        form = ctk.CTkFrame(wrapper, fg_color="#F2F0EB", corner_radius=18, border_width=1, border_color="#E3D6C4")
        form.pack(fill="x", padx=10, pady=(0, 20))

        self.en_nom = ctk.CTkEntry(form, placeholder_text="Nombre", width=420)
        self.en_nom.pack(pady=8, padx=20)

        self.en_ape = ctk.CTkEntry(form, placeholder_text="Apellido", width=420)
        self.en_ape.pack(pady=8, padx=20)

        self.en_dni = ctk.CTkEntry(form, placeholder_text="DNI", width=420)
        self.en_dni.pack(pady=8, padx=20)

        self.en_mai = ctk.CTkEntry(form, placeholder_text="Email", width=420)
        self.en_mai.pack(pady=8, padx=20)

        self.en_pass = ctk.CTkEntry(form, placeholder_text="Contraseña", width=420, show="*")
        self.en_pass.pack(pady=8, padx=20)

        self.lbl_feedback = ctk.CTkLabel(form, text="", font=("Inter", 11), text_color="#27632a")
        self.lbl_feedback.pack(pady=(5, 0))

        ctk.CTkButton(form, text="Registrar Peluquero/a", fg_color="#8B4513", hover_color="#A0522D", corner_radius=12,
                      font=("Inter", 12, "bold"), width=180, command=self.guardar_empleado).pack(pady=20)

        list_frame = ctk.CTkFrame(wrapper, fg_color="#FFFFFF", corner_radius=18, border_width=1, border_color="#E3D6C4")
        list_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        ctk.CTkLabel(list_frame, text="Empleados registrados", font=("Inter", 16, "bold"), anchor="w").pack(fill="x", padx=20, pady=(20, 10))

        self.scroll_empleados = ctk.CTkScrollableFrame(list_frame, fg_color="transparent", border_width=0)
        self.scroll_empleados.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.cargar_empleados()

    def validar_campos(self):
        nombre = self.en_nom.get().strip()
        apellido = self.en_ape.get().strip()
        dni = self.en_dni.get().strip()
        email = self.en_mai.get().strip()
        password = self.en_pass.get().strip()

        if not nombre or not apellido or not dni or not password:
            self.lbl_feedback.configure(text="Nombre, apellido, DNI y contraseña son obligatorios.", text_color="#9D2B2B")
            return False

        if email and "@" not in email:
            self.lbl_feedback.configure(text="Ingresa un email válido o déjalo vacío.", text_color="#9D2B2B")
            return False

        self.lbl_feedback.configure(text="", text_color="#27632a")
        return True

    def guardar_empleado(self):
        if not self.validar_campos():
            return

        if self.db.agregar_empleado(
                self.en_nom.get().strip(),
                self.en_ape.get().strip(),
                self.en_mai.get().strip(),
                self.en_dni.get().strip(),
                self.en_pass.get().strip()):
            self.lbl_feedback.configure(text="Empleado registrado correctamente y usuario creado.", text_color="#27632a")
            for entry in [self.en_nom, self.en_ape, self.en_dni, self.en_mai, self.en_pass]:
                entry.delete(0, 'end')
            self.cargar_empleados()
        else:
            self.lbl_feedback.configure(text="No se pudo registrar el empleado. Revisa la conexión.", text_color="#9D2B2B")

    def cargar_empleados(self):
        for widget in self.scroll_empleados.winfo_children():
            widget.destroy()

        empleados = self.db.obtener_empleados()

        if not empleados:
            ctk.CTkLabel(self.scroll_empleados, text="No hay empleados registrados aún.", font=("Inter", 12), text_color="#5C4033").pack(pady=20)
            return

        for empleado in empleados:
            nombre_completo = f"{empleado.get('nombre', '')} {empleado.get('apellido', '')}".strip()
            fila = ctk.CTkFrame(self.scroll_empleados, fg_color="#F2F0EB", corner_radius=12, border_width=1, border_color="#E3D6C4")
            fila.pack(fill="x", pady=6)

            ctk.CTkLabel(fila, text=nombre_completo.upper(), font=("Inter", 13, "bold"), anchor="w").pack(fill="x", padx=15, pady=(12, 3))
            ctk.CTkLabel(fila, text=f"DNI: {empleado.get('dni', '')}   |   Email: {empleado.get('mail', 'sin email')}", font=("Inter", 11), text_color="#5C4033", anchor="w").pack(fill="x", padx=15, pady=(0, 8))

            if empleado.get('tiene_usuario'):
                ctk.CTkLabel(fila, text="Usuario creado", font=("Inter", 11, "italic"), text_color="#27632a", anchor="w").pack(fill="x", padx=15, pady=(0, 10))
            else:
                btn = ctk.CTkButton(fila, text="Crear acceso", width=140, fg_color="#8B4513", hover_color="#A0522D", corner_radius=12,
                              font=("Inter", 11, "bold"), command=lambda emp=empleado: self.abrir_crear_usuario(emp))
                btn.pack(padx=15, pady=(0, 10), anchor="e")

    def abrir_crear_usuario(self, empleado):
        v = ctk.CTkToplevel(self.master)
        v.title("Crear usuario para empleado")
        v.geometry("420x260")
        v.attributes("-topmost", True)
        v.configure(fg_color="#FAF9F6")

        ctk.CTkLabel(v, text=f"Crear acceso para {empleado.get('nombre', '')} {empleado.get('apellido', '')}", font=("Inter", 14, "bold"), text_color="#5C4033").pack(pady=(20, 10), padx=20)
        ctk.CTkLabel(v, text=f"Usuario: {empleado.get('dni', '')}", font=("Inter", 12), text_color="#5C4033").pack(padx=20)

        self.en_pass_crear = ctk.CTkEntry(v, placeholder_text="Contraseña", width=360, show="*")
        self.en_pass_crear.pack(pady=20)

        lbl_error = ctk.CTkLabel(v, text="", font=("Inter", 11), text_color="#9D2B2B")
        lbl_error.pack(pady=(0, 10))

        def guardar_usuario():
            password = self.en_pass_crear.get().strip()
            if not password:
                lbl_error.configure(text="Debe ingresar una contraseña.")
                return
            if self.db.crear_usuario_para_empleado(empleado['idempleado'], password):
                v.destroy()
                self.lbl_feedback.configure(text=f"Usuario creado para {empleado.get('nombre', '')}.", text_color="#27632a")
                self.cargar_empleados()
            else:
                lbl_error.configure(text="No se pudo crear el usuario. Revisa la conexión.")

        ctk.CTkButton(v, text="Crear usuario", fg_color="#8B4513", hover_color="#A0522D", width=180, height=44, corner_radius=12,
                      font=("Inter", 12, "bold"), command=guardar_usuario).pack(pady=10)
