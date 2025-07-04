# Función que valida los datos ingresados por el usuario
def validar_entrada(nombre, cedula, contacto, tipo_membresia):
    
    # Verifica que el nombre contenga solo letras (se permiten espacios)
    if not nombre.replace(" ", "").isalpha():
        return False, "El nombre solo debe contener letras."

    # Verifica que la cédula tenga entre 1 y 5 caracteres alfanuméricos
    if not (1 <= len(cedula) <= 5 and cedula.isalnum()):
        return False, "La cédula debe contener hasta 5 caracteres alfanuméricos."

    # Verifica que el número de contacto tenga exactamente 8 dígitos numéricos
    if not (contacto.isdigit() and len(contacto) == 8):
        return False, "El contacto debe contener 8 dígitos numéricos."

    # Verifica que el tipo de membresía sea "mensual" o "diaria" (sin importar mayúsculas)
    if tipo_membresia.lower() not in ["mensual", "diaria"]:
        return False, "El tipo de membresía debe ser 'mensual' o 'diaria'."

    # Si todas las validaciones pasan, se devuelve True sin mensaje de error
    return True, ""
