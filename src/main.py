from database.connection import Database

def inicio():
    db = Database()
    agenda = db.obtener_agenda()
    
    print("--- Agenda de la Peluquería ---")
    if not agenda:
        print("No hay turnos registrados o error de conexión.")
    else:
        for turno in agenda:
            print(f"Fecha: {turno['Fecha_Hora']} | Cliente: {turno['Cliente']} | Servicio: {turno['Servicio']}")

if __name__ == "__main__":
    inicio()