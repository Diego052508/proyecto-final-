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
