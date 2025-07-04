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
