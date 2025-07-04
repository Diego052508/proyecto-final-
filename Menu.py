# Importa fnciones de otro mudulo.
from gestion_clientes import registrar_cliente, modificar_cliente, buscar_cliente, eliminar_cliente
from pagos import registrar_pago
from asistencias import registrar_asistencia
from reportes import generar_reportes, verificar_alertas

# Define una función para mostrar el menú principal del sistema.
def mostrar_menu():
    while True:
        print("\n--- MENÚ DEL SISTEMA GIMNASIO ---")
        print("1. Registrar nuevo cliente")
        print("2. Registrar pago")
        print("3. Registrar asistencia")
        print("4. Modificar datos de cliente")
        print("5. Buscar cliente")
        print("6. Generar reportes")
        print("7. Verificar membresías vencidas")
        print("8. Eliminar cliente")
        print("0. Salir")

        #Aqui pide que el usuario elija una funcion
        opcion = input("Seleccione una opción: ")
        
        #Segun lo elegido llama a dicha funcion

        if opcion == "1":
            registrar_cliente()
        elif opcion == "2":
            registrar_pago()
        elif opcion == "3":
            registrar_asistencia()
        elif opcion == "4":
            modificar_cliente()
        elif opcion == "5":
            buscar_cliente()
        elif opcion == "6":
            generar_reportes()
        elif opcion == "7":
            verificar_alertas()
        elif opcion == "8":
            eliminar_cliente()
        elif opcion == "0":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción inválida.")
#Aqui manda a llamar las funciones
if __name__ == "__main__":
    cargar_datos()
    mostrar_menu()
