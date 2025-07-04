from datetime import datetime, timedelta
from datos import clientes, guardar_datos

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
