import customtkinter as ctk # Agregamos el import para configurar el tema global
from ui.main_window import MainWindow
from ui.login import LoginWindow
import os

def inicio():
    # 1. Limpieza estética de la consola (opcional)
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # 2. Configuración Global de Apariencia
    # Esto asegura que tanto el Login como la MainWindow nazcan en modo claro
    ctk.set_appearance_mode("Light") 
    ctk.set_default_color_theme("blue") # El color de acento de los botones/bordes

    def mostrar_principal(usuario):
        # 1. Ocultamos el login inmediatamente para evitar colisiones de hilos
        login.withdraw() 
        
        # 2. Creamos la ventana principal
        app = MainWindow(usuario)
        
        # 3. Protocolo de cierre total: Limpia el login oculto al cerrar la app
        app.protocol("WM_DELETE_WINDOW", lambda: (app.quit(), app.destroy(), login.destroy()))
        
        app.mainloop()

    # 3. Lanzamiento del Login
    login = LoginWindow(on_login_success=mostrar_principal)
    login.mainloop()

if __name__ == "__main__":
    inicio()