import subprocess
import os
import signal
import time
#7770
PUERTO_A_USAR = 7770

def state_port():
    result = subprocess.run(f"sudo ufw status | grep {PUERTO_A_USAR}",shell=True, capture_output=True, text=True)
    lista = result.stdout.splitlines()

    if "ALLOW" in lista[0] and "ALLOW" in lista[1]:
        print(f"El puerto {PUERTO_A_USAR} está abierto.")
        return True
    else:
        print(f"El puerto {PUERTO_A_USAR} está cerrado.")
        return False

def levantar_servicio():
    if state_port():
        activate_command = "source venv/bin/activate"
        uvicorn_command = f"uvicorn main:app --host 0.0.0.0 --port {PUERTO_A_USAR} --reload"

        # Combina ambos comandos en uno solo utilizando el operador de cadena
        full_command = f"{activate_command} && {uvicorn_command}"

        # Ejecuta el comando en el mismo terminal y mantiene el proceso en ejecución
        subprocess.call(["bash", "-c", full_command])
        print("Presiona Ctrl+C para detener el servidor...")
        

def levantar_servicio_seguro():
    if state_port():
        activate_command = "source venv/bin/activate"
        
        uvicorn_command = f"uvicorn main:app --ssl-keyfile=./keys/server.key --ssl-certfile=./keys/server.crt --host 0.0.0.0 --port {PUERTO_A_USAR}"

        # Combina ambos comandos en uno solo utilizando el operador de cadena
        full_command = f"{activate_command} && {uvicorn_command}"

        # Ejecuta el comando en el mismo terminal y mantiene el proceso en ejecución
        subprocess.call(["bash", "-c", full_command])
        print("Presiona Ctrl+C para detener el servidor...")

        

def open_port():
    if not state_port():
        subprocess.run(["sudo", "ufw", "allow", str(PUERTO_A_USAR)])
        print("Puerto abierto correctamente.")
    else:
        print("El puerto ya está abierto.")

def close_port():
    if state_port():
        subprocess.run(["sudo", "ufw", "deny", str(PUERTO_A_USAR)])
        print("Puerto cerrado correctamente.")
    else:
        print("El puerto ya está cerrado.")

while True:
    print("Menú:")
    print("1. Estado del puerto")
    print("2. Abrir Puerto")
    print("3. Cerrar Puerto")
    print("4. Levantar servicio")
    print("5. Levantar servicio seguro")
    print("6. Salir")

    opcion = input("Selecciona una opción (1-6): ")

    if opcion == "1":
        state_port()
    elif opcion == "2":
        open_port()
    elif opcion == "3":
        close_port()
    elif opcion == "4":
        levantar_servicio()
    elif opcion == "5":
        levantar_servicio_seguro()
    elif opcion == "6":
        print("Saliendo del menú. ¡Hasta luego!")
        break
    else:
        print("Opción no válida. Por favor, selecciona una opción válida.")

