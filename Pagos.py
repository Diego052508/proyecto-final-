# Importa las clases datetime y timedelta para manejar fechas y tiempos
from datetime import datetime, timedelta

# Importa los datos de clientes y la función para guardar datos desde otro archivo llamado datos.py
from datos import clientes, guardar_datos

# Define la función principal para registrar un pago de un cliente
def registrar_pago():
    # Solicita al usuario la cédula del cliente
    cedula = input("Cédula del cliente: ")

    # Verifica si la cédula existe en el diccionario de clientes
    if cedula not in clientes:
        print("Cliente no encontrado.")  # Muestra mensaje si no se encuentra
        return  # Sale de la función

    try:
        # Intenta convertir el monto ingresado a tipo float
        monto = float(input("Monto pagado: "))
    except ValueError:
        # Si no se puede convertir, muestra un mensaje de error
        print("Monto inválido.")
        return

    # Registra la fecha y hora actual del pago
    fecha_pago = datetime.now()

    # Accede al cliente por cédula
    cliente = clientes[cedula]

    # Agrega el pago a la lista de pagos del cliente
    cliente['pagos'].append({'fecha': fecha_pago, 'monto': monto})

    # Establece la nueva fecha de renovación (60 segundos después del pago, solo como ejemplo)
    cliente['fecha_renovacion'] = fecha_pago + timedelta(seconds=60)

    # Marca al cliente como activo
    cliente['activo'] = True

    # Guarda los datos actualizados (probablemente en un archivo JSON o base de datos)
    guardar_datos()

    # Muestra mensaje de confirmación
    print(f"\nPago registrado para {cliente['nombre']} el {fecha_pago.date()}.\n")

    # ---------- INICIO BLOQUE REPETIDO INNECESARIAMENTE ----------
    # Este bloque se repite exactamente igual y no es necesario
    fecha_pago = datetime.now()
    cliente =
