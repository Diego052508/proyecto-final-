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
