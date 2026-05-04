import customtkinter as ctk
from ui.tabs.agenda_tab import AgendaTab
from ui.tabs.clientes_tab import ClientesTab
from ui.tabs.servicios_tab import ServiciosTab
from ui.tabs.stock_tab import StockTab
from ui.tabs.caja_tab import CajaTab
from ui.tabs.stats_tab import StatsTab
from ui.tabs.config import ConfigTab
class MainWindow(ctk.CTk):
    def __init__(self, usuario):
        super().__init__()
        self.usuario_actual = usuario
        self.title("Peluquería - Gestión Integral")
        self.geometry("1100x850")
        ctk.set_appearance_mode("Light") 
        self.configure(fg_color="#FAF9F6")

        self.tabview = ctk.CTkTabview(self, segmented_button_fg_color="#F2F0EB", 
                                      segmented_button_selected_color="#D2B48C", 
                                      text_color="black")
        self.tabview.pack(pady=10, padx=10, fill="both", expand=True)

        # Inicialización de pestañas modularizadas
        self.tab_agenda = AgendaTab(self.tabview.add("📅 Agenda"), self)
        self.tab_clientes = ClientesTab(self.tabview.add("👥 Clientes"), self)
        self.tab_servicios = ServiciosTab(self.tabview.add("✂️ Precios"), self)
        self.tab_stock = StockTab(self.tabview.add("📦 Stock"), self)

        if self.usuario_actual['rol'] == 'admin':
            self.tab_caja_obj = CajaTab(self.tabview.add("💰 Caja"), self)
            self.tab_config = ConfigTab(self.tabview.add("⚙️ Config."), self)
            self.tab_stats_obj = StatsTab(self.tabview.add("📊 Estadísticas"), self)
            
            
        self.btn_logout = ctk.CTkButton(self, text="Cerrar Sesión 🔓", 
                                        fg_color="#CD5C5C", hover_color="#A52A2A",
                                        width=120, height=30, command=self.cerrar_sesion)
        self.btn_logout.place(relx=0.98, rely=0.02, anchor="ne")

    

    def cerrar_sesion(self):
        from tkinter import messagebox
        if messagebox.askyesno("Cerrar Sesión", "¿Estás seguro que querés salir?"):
            # 1. Cerramos la ventana actual y salimos del mainloop
            self.quit()
            self.destroy()
            
            # 2. Importación diferida para evitar errores de importación circular[cite: 11]
            from ui.login import LoginWindow
            
            def reiniciar():
                def relog(usuario):
                    # Importamos aquí mismo para que el ciclo de reinicio sea limpio
                    from ui.main_window import MainWindow
                    app = MainWindow(usuario)
                    app.mainloop()
                
                # 3. Reabrimos la ventana de login pasándole la función de éxito[cite: 11]
                nuevo_login = LoginWindow(on_login_success=relog)
                nuevo_login.mainloop()
            
            reiniciar()

    
