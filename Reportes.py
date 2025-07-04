from datetime import datetime, timedelta
from datos import clientes, asistencias, guardar_datos

# Función para generar reportes de asistencia y pagos de los clientes
def generar_reportes():
    print("\n--- Generar Reportes de Asistencia ---")
    print("1. Reporte semanal")
    print("2. Reporte mensual")
    
    # El usuario elige el tipo de reporte
    opcion = input("Seleccione una opción: ")

    hoy = datetime.now()  # Se obtiene la fecha y hora actual

    # Dependiendo de la opción elegida, se calcula la fecha de inicio del reporte
    if opcion == "1":
        desde_fecha = hoy - timedelta(days=7)  # Últimos 7 días
        titulo = "--- Reporte Semanal ---"
    elif opcion == "2":
        desde_fecha = hoy - timedelta(days=30)  # Últimos 30 días
        titulo = "--- Reporte Mensual ---"
    else:
        print("Opción inválida.")  # Si no se elige 1 ni 2, se sale
        return

    # Se inicializa la lista que almacenará el contenido del reporte
    reporte = [titulo + "\n"]
    print(titulo + "\n")

    # ----- Sección de asistencias -----
    reporte.append("--- Asistencias ---")
    print("--- Asistencias ---")
    
    # Se recorren todas las asistencias registradas
    for asistencia in asistencias:
        # Si la fecha de la asistencia es dentro del rango del reporte
        if asistencia['fecha'] >= desde_fecha:
            # Se obtiene el nombre del cliente según su cédula
            nombre = clientes.get(asistencia['cedula'], {}).get('nombre', 'Desconocido')
            # Se genera una línea informativa
            linea = f"{nombre} asistió el {asistencia['fecha'].date()}"
            print(linea)
            reporte.append(linea)

    # ----- Sección de pagos -----
    reporte.append("\n--- Pagos por Membresía ---")
    print("\n--- Pagos por Membresía ---")

    # Inicializa contadores para los pagos por tipo de membresía
    total_mensual = 0
    total_diaria = 0

    # Recorre todos los clientes
    for cliente in clientes.values():
        # Recorre todos los pagos de ese cliente
        for pago in cliente['pagos']:
            # Verifica si el pago es dentro del rango del reporte
            if pago['fecha'] >= desde_fecha:
                # Se escribe la línea de reporte del pago
                linea = f"{cliente['nombre']} pagó {pago['monto']} C$ el {pago['fecha'].date()}"
                print(linea)
                reporte.append(linea)

                # Acumula los pagos según el tipo de membresía
                if cliente['tipo_membresia'] == 'mensual':
                    total_mensual += pago['monto']
                elif cliente['tipo_membresia'] == 'diaria':
                    total_diaria += pago['monto']

    # Se agregan las líneas de totales al reporte y se muestran en pantalla
    linea_mensual = f"Total Pagado por membresía mensual: {total_mensual} C$"
    linea_diaria = f"Total Pagado por membresía diaria: {total_diaria} C$"
    print(linea_mensual)
    print(linea_diaria)
    reporte.append(linea_mensual)
    reporte.append(linea_diaria)

    # ----- Sección de estado de clientes -----
    reporte.append("\n--- Estado de Clientes ---")
    print("\n--- Estado de Clientes ---")

    # Recorre todos los clientes y muestra si están activos o no
    for cedula, cliente in clientes.items():
        estado = "Activo" if cliente['activo']
