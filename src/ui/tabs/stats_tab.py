import customtkinter as ctk
from database.connection import Database
from datetime import datetime
from tkinter import filedialog, messagebox
import pandas as pd

class StatsTab:
    def __init__(self, master, parent):
        self.master = master  # El tab físico
        self.parent = parent  # MainWindow
        self.db = Database()
        self.setup_ui()

    def setup_ui(self):
        """Define la interfaz de reportes y selector de periodos[cite: 7]"""
        f_top = ctk.CTkFrame(self.master, fg_color="transparent")
        f_top.pack(pady=20, fill="x", padx=50)
        
        ctk.CTkLabel(f_top, text="REPORTES DE INGRESOS", font=("Inter", 22, "bold")).pack(side="left")
        
        # Botón para exportar Excel
        ctk.CTkButton(f_top, text="📊 Exportar Excel (CSV)", fg_color="#8B4513", hover_color="#A0522D", corner_radius=10,
                      font=("Inter", 12, "bold"), command=self.exportar_estadisticas_excel).pack(side="right", padx=10)
        
        self.selector_periodo = ctk.CTkComboBox(f_top, values=["Semanal", "Mensual", "Anual"], 
                                                command=lambda _: self.actualizar_grafico())
        self.selector_periodo.set("Mensual")
        self.selector_periodo.pack(side="right")

        self.frame_grafico = ctk.CTkFrame(self.master, fg_color="#F2F0EB", corner_radius=15)
        self.frame_grafico.pack(pady=10, padx=50, fill="both", expand=True)
        self.actualizar_grafico()

    def actualizar_grafico(self):
        for widget in self.frame_grafico.winfo_children(): widget.destroy()
        
        periodo = self.selector_periodo.get()
        datos = Database().obtener_estadisticas_ingresos(periodo)

        if not datos:
            ctk.CTkLabel(self.frame_grafico, text=f"No hay datos suficientes para el reporte {periodo.lower()}.").pack(pady=100)
            return

        # Generamos barritas visuales simples[cite: 5]
        max_valor = max(float(d['total']) for d in datos) if datos else 1
        
        for d in datos:
            row = ctk.CTkFrame(self.frame_grafico, fg_color="transparent")
            row.pack(fill="x", padx=30, pady=10)
            
            ctk.CTkLabel(row, text=str(d['etiqueta']).upper(), width=100, anchor="w").pack(side="left")
            
            # Calculamos el ancho de la barra proporcional al total[cite: 5]
            ancho_barra = (float(d['total']) / max_valor) * 400
            ctk.CTkFrame(row, width=ancho_barra, height=20, fg_color="#D2B48C", corner_radius=5).pack(side="left", padx=10)
            
            ctk.CTkLabel(row, text=f"$ {d['total']}", font=("Inter", 12, "bold")).pack(side="left")


    def exportar_estadisticas_excel(self):
        from tkinter import filedialog, messagebox
        import pandas as pd
        
        db = Database()
        datos = db.obtener_pagos_para_exportar()
        
        if not datos:
            messagebox.showinfo("Exportar", "No hay datos de ventas para exportar.")
            return
            
        path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel Workbook", "*.xlsx")],
            initialfile=f"Reporte_Ventas_{datetime.now().strftime('%d_%m_%Y')}.xlsx"
        )
        
        if path:
            try:
                # 1. Creamos el DataFrame
                df = pd.DataFrame(datos)
                df.columns = ['ID Pago', 'Fecha y Hora', 'Monto ($)', 'Método de Pago', 'Servicio']
                
                # 2. Usamos un "ExcelWriter" para poder aplicar formatos
                with pd.ExcelWriter(path, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='Ventas')
                    
                    # 3. Auto-ajuste de columnas automático
                    worksheet = writer.sheets['Ventas']
                    for idx, col in enumerate(df.columns):
                        # Encontramos el largo máximo del contenido en esa columna
                        max_len = max(
                            df[col].astype(str).map(len).max(),
                            len(col)
                        ) + 2 # Margen extra
                        worksheet.column_dimensions[chr(65 + idx)].width = max_len
                
                messagebox.showinfo("Éxito", f"Reporte profesional generado en:\n{path}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo generar el Excel: {e}")