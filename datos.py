from datetime import datetime, timedelta
import os

ARCHIVO_CLIENTES = "clientes.txt"
ARCHIVO_ASISTENCIAS = "asistencias.txt"

clientes = {}       # Diccionario que almacenará los datos de los clientes
asistencias = []    # Lista que almacenará los registros de asistencias

# Función para cargar los datos desde los archivos 'clientes.txt' y 'asistencias.txt'
def cargar_datos():
    global clientes, asistencias

    # Verifica si el archivo de clientes existe
    if os.path.exists(ARCHIVO_CLIENTES):
        with open(ARCHIVO_CLIENTES, "r", encoding="utf-8") as f:
            for linea in f:
                partes = linea.strip().split("|")
                if len(partes) >= 7:
                    # Extrae y limpia los datos de cada campo
                    nombre = partes[0].split(":")[1].strip()
                    cedula = partes[1].split(":")[1].strip()
                    contacto = partes[2].split(":")[1].strip()
                    tipo = partes[3].split(":")[1].strip()
                    inicio = datetime.strptime(partes[4].split(":")[1].strip(), "%Y-%m-%d")
                    renovacion = datetime.strptime(partes[5].split(":")[1].strip(), "%Y-%m-%d")
                    estado = partes[6].split(":")[1].strip()

                    # Guarda los datos del cliente en el diccionario
                    clientes[cedula] = {
                        'nombre': nombre,
                        'contacto': contacto,
                        'tipo_membresia': tipo,
                        'fecha_inicio': inicio,
                        'fecha_renovacion': renovacion,
                        'pagos': [],  # Inicializa pagos como lista vacía
                        'activo': estado == "Activo"  # Convierte el estado en booleano
                    }

    # Verifica si el archivo de asistencias existe
    if os.path.exists(ARCHIVO_ASISTENCIAS):
        with open(ARCHIVO_ASISTENCIAS, "r", encoding="utf-8") as f:
            for linea in f:
                partes = linea.strip().split("|")
                if len(partes) >= 3:
                    cedula = partes[0].split(":")[1].strip()
                    fecha_str = partes[2].split(":")[1].strip()
                    # Convierte la fecha de texto a objeto datetime y guarda la asistencia
                    asistencias.append({
                        "cedula": cedula,
                        "fecha": datetime.strptime(fecha_str, "%Y-%m-%d")
                    })

# Función para guardar los datos actualizados de clientes y asistencias en sus archivos respectivos
def guardar_datos():
    # Guarda los datos de clientes
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

    # Guarda los datos de asistencias
    with open(ARCHIVO_ASISTENCIAS, "w", encoding="utf-8") as f:
        for a in asistencias:
            # Se obtiene el nombre del cliente usando su cédula, o 'Desconocido' si no existe
            nombre = clientes.get(a["cedula"], {}).get("nombre", "Desconocido")
            f.write(f"Cédula: {a['cedula']} | Nombre: {nombre} | Fecha: {a['fecha'].date()}\n")

