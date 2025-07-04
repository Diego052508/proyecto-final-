from datetime import datetime, timedelta
from datos import clientes, guardar_datos

# Registra el pago de un cliente, actualizando la renovación y el estado activo
def registrar_pago():
    cedula = input("Cédula del cliente: ")
    if cedula not in clientes:
        print("Cliente no encontrado.")
        return
# Valida que le monto que entra sea valido
    try:
        monto = float(input("Monto pagado: "))
    except ValueError:
        print("Monto inválido.") 
        return

    fecha_pago = datetime.now()
    cliente = clientes[cedula]
    cliente['pagos'].append({'fecha': fecha_pago, 'monto': monto})# Se guarda el pago con fecha y monto
    cliente['fecha_renovacion'] = fecha_pago + timedelta(days=30) # Se actualiza la fecha de renovación y estado
    cliente['activo'] = True
    guardar_datos()
    print(f"\nPago registrado para {cliente['nombre']} el {fecha_pago.date()}.\n")
