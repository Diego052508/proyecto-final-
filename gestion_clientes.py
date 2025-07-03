def registrar_cliente():
    nombre = input("Nombre del cliente: ")
    cedula = input("Cédula del cliente: ")
    contacto = input("Teléfono o contacto: ")
    tipo_membresia = input("Tipo de membresía (mensual o diaria): ")

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

def eliminar_cliente():
    cedula = input("Cédula del cliente a eliminar: ")
    from datos import asistencias  # evitar import circular
    if cedula in clientes:
        del clientes[cedula]
        asistencias[:] = [a for a in asistencias if a['cedula'] != cedula]
        guardar_datos()
        print("Cliente y asistencias eliminados exitosamente.")
    else:
        print("Cliente no encontrado.")
