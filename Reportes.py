from datetime import datetime, timedelta
from datos import clientes, asistencias, guardar_datos

def generar_reportes():
    print("\n--- Generar Reportes de Asistencia ---")
    print("1. Reporte semanal")
    print("2. Reporte mensual")
    opcion = input("Seleccione una opción: ")

    hoy = datetime.now()
    if opcion == "1":
        desde_fecha = hoy - timedelta(days=7)
        titulo = "--- Reporte Semanal ---"
    elif opcion == "2":
        desde_fecha = hoy - timedelta(days=30)
        titulo = "--- Reporte Mensual ---"
    else:
        print("Opción inválida.")
        return

    reporte = [titulo + "\n"]
    print(titulo + "\n")

    reporte.append("--- Asistencias ---")
    print("--- Asistencias ---")
    for asistencia in asistencias:
        if asistencia['fecha'] >= desde_fecha:
            nombre = clientes.get(asistencia['cedula'], {}).get('nombre', 'Desconocido')
            linea = f"{nombre} asistió el {asistencia['fecha'].date()}"
            print(linea)
            reporte.append(linea)

    reporte.append("\n--- Pagos por Membresía ---")
    print("\n--- Pagos por Membresía ---")
    total_mensual = 0
    total_diaria = 0
    for cliente in clientes.values():
        for pago in cliente['pagos']:
            if pago['fecha'] >= desde_fecha:
                linea = f"{cliente['nombre']} pagó {pago['monto']} C$ el {pago['fecha'].date()}"
                print(linea)
                reporte.append(linea)
                if cliente['tipo_membresia'] == 'mensual':
                    total_mensual += pago['monto']
                elif cliente['tipo_membresia'] == 'diaria':
                    total_diaria += pago['monto']
    linea_mensual = f"Total Pagado por membresía mensual: {total_mensual} C$"
    linea_diaria = f"Total Pagado por membresía diaria: {total_diaria} C$"
    print(linea_mensual)
    print(linea_diaria)
    reporte.append(linea_mensual)
    reporte.append(linea_diaria)

    reporte.append("\n--- Estado de Clientes ---")
    print("\n--- Estado de Clientes ---")
    for cedula, cliente in clientes.items():
        estado = "Activo" if cliente['activo'] else "Inactivo"
        linea = f"{cliente['nombre']} - {estado}"
        print(linea)
        reporte.append(linea)

    with open("reporte_semanal.txt" if opcion == "1" else "reporte_mensual.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(reporte))
        
def verificar_alertas():
    hoy = datetime.now()
    for cliente in clientes.values():
        if cliente['fecha_renovacion'] < hoy:
            cliente['activo'] = False
    guardar_datos()
    print("\nVerificación completada. Clientes con membresía vencida fueron marcados como inactivos.\n")
