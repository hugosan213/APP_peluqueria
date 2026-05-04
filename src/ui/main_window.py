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

        top_bar = ctk.CTkFrame(self, fg_color="#E7D3B8", corner_radius=18, border_width=1, border_color="#C3AA83")
        top_bar.pack(pady=10, padx=10, fill="x")

        self.btn_logout = ctk.CTkButton(top_bar, text="Cerrar Sesión 🔓", 
                                        fg_color="#8B4513", hover_color="#A0522D",
                                        width=150, height=38, corner_radius=14,
                                        font=("Inter", 12, "bold"), command=self.cerrar_sesion)
        self.btn_logout.pack(side="right", padx=16, pady=10)

        self.tabview = ctk.CTkTabview(self, fg_color="#F7E8D9", corner_radius=18,
                                      border_width=1, border_color="#C3AA83",
                                      segmented_button_fg_color="#F1D9B5", 
                                      segmented_button_selected_color="#8B4513", 
                                      text_color="black")
        self.tabview.pack(pady=(0, 10), padx=10, fill="both", expand=True)

        # Inicialización de pestañas modularizadas
        self.tab_agenda = AgendaTab(self.tabview.add("📅 Agenda"), self)
        self.tab_clientes = ClientesTab(self.tabview.add("👥 Clientes"), self)
        self.tab_servicios = ServiciosTab(self.tabview.add("✂️ Precios"), self)
        self.tab_stock = StockTab(self.tabview.add("📦 Stock"), self)

        if self.usuario_actual['rol'] == 'admin':
            self.tab_caja_obj = CajaTab(self.tabview.add("💰 Caja"), self)
            self.tab_config = ConfigTab(self.tabview.add("⚙️ Config."), self)
            self.tab_stats_obj = StatsTab(self.tabview.add("📊 Estadísticas"), self)

    

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

    
