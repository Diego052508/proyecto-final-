from datetime import datetime, timedelta
import os

ARCHIVO_CLIENTES = "clientes.txt"
ARCHIVO_ASISTENCIAS = "asistencias.txt"

clientes = {}
asistencias = []

def cargar_datos():
    global clientes, asistencias
    if os.path.exists(ARCHIVO_CLIENTES):
        with open(ARCHIVO_CLIENTES, "r", encoding="utf-8") as f:
            for linea in f:
                partes = linea.strip().split("|")
                if len(partes) >= 7:
                    nombre = partes[0].split(":")[1].strip()
                    cedula = partes[1].split(":")[1].strip()
                    contacto = partes[2].split(":")[1].strip()
                    tipo = partes[3].split(":")[1].strip()
                    inicio = datetime.strptime(partes[4].split(":")[1].strip(), "%Y-%m-%d")
                    renovacion = datetime.strptime(partes[5].split(":")[1].strip(), "%Y-%m-%d")
                    estado = partes[6].split(":")[1].strip()
                    clientes[cedula] = {
                        'nombre': nombre,
                        'contacto': contacto,
                        'tipo_membresia': tipo,
                        'fecha_inicio': inicio,
                        'fecha_renovacion': renovacion,
                        'pagos': [],
                        'activo': estado == "Activo"
                    }

    if os.path.exists(ARCHIVO_ASISTENCIAS):
        with open(ARCHIVO_ASISTENCIAS, "r", encoding="utf-8") as f:
            for linea in f:
                partes = linea.strip().split("|")
                if len(partes) >= 3:
                    cedula = partes[0].split(":")[1].strip()
                    fecha_str = partes[2].split(":")[1].strip()
                    asistencias.append({"cedula": cedula, "fecha": datetime.strptime(fecha_str, "%Y-%m-%d")})



def guardar_datos():
    with open(ARCHIVO_CLIENTES, "w", encoding="utf-8") as f:
        for cedula, cliente in clientes.items():
            f.write(
                f"Nombre: {cliente['nombre']} | "
                f"Cédula: {cedula} | "
                f"Contacto: {cliente['contacto']} | "
                f"Membresía: {cliente['tipo_membresia']} | "
                f"Inicio: {cliente['fecha_inicio'].date()} | "
                f"Renovación: {cliente['fecha_renovacion'].date()} | "
                f"Estado: {'Activo' if cliente['activo'] else 'Inactivo'}\n"
            )

    with open(ARCHIVO_ASISTENCIAS, "w", encoding="utf-8") as f:
        for a in asistencias:
            nombre = clientes.get(a["cedula"], {}).get("nombre", "Desconocido")
            f.write(f"Cédula: {a['cedula']} | Nombre: {nombre} | Fecha: {a['fecha'].date()}\n")

def validar_entrada(nombre, cedula, contacto, tipo_membresia):
    if not nombre.replace(" ", "").isalpha():
        return False, "El nombre solo debe contener letras."
    if not (1 <= len(cedula) <= 5 and cedula.isalnum()):
        return False, "La cédula debe contener hasta 5 caracteres alfanuméricos."
    if not (contacto.isdigit() and len(contacto) == 8):
        return False, "El contacto debe contener 8 dígitos numéricos."
    if tipo_membresia.lower() not in ["mensual", "diaria"]:
        return False, "El tipo de membresía debe ser 'mensual' o 'diaria'."
    return True, ""

    valido, mensaje = validar_entrada(nombre, cedula, contacto, tipo_membresia)
    if not valido:
        print(mensaje)
        return

    fecha_inicio = datetime.now()
    clientes[cedula] = {
        'nombre': nombre,
        'contacto': contacto,
        'tipo_membresia': tipo_membresia,
        'fecha_inicio': fecha_inicio,
        'fecha_renovacion': fecha_inicio,
        'pagos': [],
        'activo': False
    }
    guardar_datos()
    print(f"\n Cliente {nombre} registrado como INACTIVO el {fecha_inicio.date()}.\n")

def registrar_pago():
    cedula = input("Cédula del cliente: ")
    if cedula not in clientes:
        print("Cliente no encontrado.")
        return

    try:
        monto = float(input("Monto pagado: "))
    except ValueError:
        print("Monto inválido.")
        return
    
   

    fecha_pago = datetime.now()
    cliente = clientes[cedula]
    cliente['pagos'].append({'fecha': fecha_pago, 'monto': monto})
    cliente['fecha_renovacion'] = fecha_pago + timedelta(seconds=60)
    cliente['activo'] = True
    guardar_datos()
    print(f"\nPago registrado para {cliente['nombre']} el {fecha_pago.date()}.\n")

def registrar_asistencia():
    cedula = input("Cédula del cliente: ")
    if cedula not in clientes:
        print("Cliente no encontrado.")
        return

    cliente = clientes[cedula]
    if not cliente['activo']:
        print("Cliente con membresía vencida o inactiva.")
        return

    asistencias.append({'cedula': cedula, 'fecha': datetime.now()})
    guardar_datos()
    print(f"\nAsistencia registrada para {cliente['nombre']}.\n")

def modificar_cliente():
    cedula = input("Ingrese la cédula del cliente a modificar: ")
    if cedula not in clientes:
        print("Cliente no encontrado.")
        return

    cliente = clientes[cedula]
    print(f"Datos actuales: Nombre: {cliente['nombre']}, Contacto: {cliente['contacto']}, Membresía: {cliente['tipo_membresia']}")

    nuevo_nombre = input("Nuevo nombre (dejar vacío para no modificar): ")
    nuevo_contacto = input("Nuevo contacto (dejar vacío para no modificar): ")
    nuevo_tipo = input("Nuevo tipo de membresía (mensual o diaria, dejar vacío para no modificar): ")

    if nuevo_nombre:
        cliente['nombre'] = nuevo_nombre
    if nuevo_contacto:
        cliente['contacto'] = nuevo_contacto
    if nuevo_tipo.lower() in ["mensual", "diaria"]:
        cliente['tipo_membresia'] = nuevo_tipo

    guardar_datos()
    print("Datos actualizados correctamente.")

def buscar_cliente():
    cedula = input("Ingrese la cédula del cliente a buscar: ")
    if cedula in clientes:
        c = clientes[cedula]
        print(f"Nombre: {c['nombre']}\nContacto: {c['contacto']}\nMembresía: {c['tipo_membresia']}\nEstado: {'Activo' if c['activo'] else 'Inactivo'}\nInicio: {c['fecha_inicio'].date()}\nRenovación: {c['fecha_renovacion'].date()}")
    else:
        print("Cliente no encontrado.")

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
    inactivos = []
    for cliente in clientes.values():
        if cliente['fecha_renovacion'] < hoy:
            cliente['activo'] = False
    guardar_datos()
    print("\nVerificación completada. Clientes con membresía vencida fueron marcados como inactivos.\n")
    if inactivos:
        print("Clientes inactivos:")
        for nombre in inactivos:
            print("-", nombre)
    else:
        print("No hay clientes inactivos.")


def eliminar_cliente():
    cedula = input("Cédula del cliente a eliminar: ")
    if cedula in clientes:
        del clientes[cedula]
        global asistencias
        asistencias = [a for a in asistencias if a['cedula'] != cedula]
        guardar_datos()
        print("Cliente y asistencias eliminados exitosamente.")
    else:
        print("Cliente no encontrado.")


def menu():
    while True:
        print("\n--- MENÚ DEL SISTEMA GIMNASIO ---")
        print("1. Registrar nuevo cliente")
        print("2. Registrar pago")
        print("3. Registrar asistencia")
        print("4. Modificar datos de cliente")
        print("5. Buacar cliente")
        print("6. Generar reportes")
        print("7. Verificar membresías vencidas")
        print("8. Eliminar cliente")
        print("0. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_cliente()
        elif opcion == "2":
            registrar_pago()
        elif opcion == "3":
            registrar_asistencia()
        elif opcion == "4":
            modificar_cliente()
        elif opcion == "5":
            buscar_cliente()
        elif opcion == "6":
            generar_reportes()
        elif opcion == "7":
            verificar_alertas()
        elif opcion == "8":
            eliminar_cliente()
        elif opcion == "0":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menu()
