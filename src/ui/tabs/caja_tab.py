import customtkinter as ctk
from database.connection import Database
from tkinter import messagebox

class CajaTab:
    def __init__(self, master, parent):
        self.master = master  # El tab físico (ctk.CTkFrame)[cite: 19]
        self.parent = parent  # Instancia de MainWindow[cite: 19]
        self.db = Database()
        self.setup_ui()

    def setup_ui(self):
        """Define la estructura de la caja diaria[cite: 7]"""
        for widget in self.master.winfo_children(): 
            widget.destroy()
        
        f_top = ctk.CTkFrame(self.master, fg_color="transparent")
        f_top.pack(pady=20, fill="x", padx=50)
        
        ctk.CTkLabel(f_top, text="CONTROL DE CAJA DIARIA", font=("Inter", 22, "bold")).pack(side="left")
        ctk.CTkButton(f_top, text="- Retirar Dinero / Gasto", fg_color="#CD5C5C", hover_color="#A52A2A", corner_radius=10,
                      font=("Inter", 12, "bold"), command=self.abrir_formulario_egreso).pack(side="right")
        
        self.frame_caja_info = ctk.CTkFrame(self.master, fg_color="#F2F0EB", corner_radius=15)
        self.frame_caja_info.pack(pady=10, padx=50, fill="both", expand=True)
        self.cargar_caja_diaria()

    def cargar_caja_diaria(self):
        """Refresca los ingresos y egresos del día[cite: 7]"""
        for widget in self.frame_caja_info.winfo_children(): 
            widget.destroy()
            
        ingresos = self.db.obtener_caja_diaria()
        egresos_total = self.db.obtener_total_egresos_hoy()
        total_ingresos = sum(float(r['total']) for r in ingresos)
        
        ctk.CTkLabel(self.frame_caja_info, text="INGRESOS", font=("Inter", 14, "bold")).pack(pady=(10,5))
        for r in ingresos:
            card = ctk.CTkFrame(self.frame_caja_info, fg_color="#FFFFFF")
            card.pack(fill="x", padx=40, pady=2)
            ctk.CTkLabel(card, text=f"{r['tipoPago'].upper()}: $ {r['total']}").pack(pady=5)

        ctk.CTkFrame(self.frame_caja_info, height=2, fg_color="#D2B48C").pack(fill="x", padx=30, pady=15)
        ctk.CTkLabel(self.frame_caja_info, text=f"TOTAL EGRESOS: - $ {egresos_total}", 
                     text_color="#CD5C5C", font=("Inter", 16, "bold")).pack()

        saldo_neto = total_ingresos - float(egresos_total)
        ctk.CTkLabel(self.frame_caja_info, text=f"SALDO EN CAJA: $ {saldo_neto}", 
                     font=("Inter", 26, "bold"), text_color="#2D2424").pack(pady=20)

    def abrir_formulario_egreso(self):
        """Seguridad y formulario de retiro[cite: 7, 8]"""
        dialogo = ctk.CTkInputDialog(text="Ingrese su contraseña para autorizar el retiro:", title="Seguridad de Caja")
        password_ingresada = dialogo.get_input()

        # CORRECCIÓN: Accedemos al password a través de self.parent
        if password_ingresada == self.parent.usuario_actual.get('password'):
            # CORRECCIÓN: Usamos self.master como contenedor de la ventana
            v = ctk.CTkToplevel(self.master)
            v.geometry("350x400")
            v.attributes("-topmost", True)
            v.title("Nuevo Egreso")
            
            ctk.CTkLabel(v, text="SALIDA DE DINERO", font=("Inter", 16, "bold")).pack(pady=20)
            
            em = ctk.CTkEntry(v, placeholder_text="Monto", width=250)
            em.pack(pady=10)
            
            ed = ctk.CTkEntry(v, placeholder_text="Descripción", width=250)
            ed.pack(pady=10)
            
            def guardar():
                monto = em.get()
                desc = ed.get()
                if not monto or not desc:
                    messagebox.showwarning("Atención", "Complete todos los campos.")
                    return
                
                if self.db.registrar_egreso(monto, desc):
                    v.destroy()
                    self.cargar_caja_diaria()
            
            ctk.CTkButton(v, text="Confirmar Gasto", fg_color="#CD5C5C", hover_color="#A52A2A", corner_radius=8, command=guardar).pack(pady=30)
            
        elif password_ingresada is not None:
            messagebox.showerror("Error", "Contraseña incorrecta. Operación cancelada.")