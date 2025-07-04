from datetime import datetime, timedelta
from datos import clientes, asistencias, guardar_datos

def generar_reportes():

def verificar_alertas():
    hoy = datetime.now()
    for cliente in clientes.values():
        if cliente['fecha_renovacion'] < hoy:
            cliente['activo'] = False
    guardar_datos()
    print("\nVerificación completada. Clientes con membresía vencida fueron marcados como inactivos.\n")
