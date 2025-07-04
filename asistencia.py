from datetime import datetime
from datos import clientes, asistencias, guardar_datos

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
