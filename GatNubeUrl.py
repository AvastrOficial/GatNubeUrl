import os
import requests
from colorama import init, Fore, Style
import subprocess

# Inicializar colorama
init(autoreset=True)

# Configuración de URLs
CATBOX_HOST = "https://catbox.moe/user/api.php"
LITTER_HOST = "https://litterbox.catbox.moe/resources/internals/api.php"

# Función para cargar el archivo
def cargar_archivo(opcion, ruta_archivo, expiracion=None):
    if not os.path.exists(ruta_archivo):
        print(Fore.RED + "Archivo no encontrado.")
        return

    try:
        with open(ruta_archivo, 'rb') as archivo_a_subir:
            archivos = {'fileToUpload': archivo_a_subir}
            datos = {'reqtype': 'fileupload'}

            if opcion == 'catbox':
                respuesta = requests.post(CATBOX_HOST, files=archivos, data=datos)
            elif opcion == 'litterbox':
                if not expiracion:
                    print(Fore.RED + "Por favor, proporciona un tiempo de expiración para Litterbox.")
                    return
                datos['time'] = expiracion
                respuesta = requests.post(LITTER_HOST, files=archivos, data=datos)
            else:
                print(Fore.RED + "Opción inválida seleccionada.")
                return

            if respuesta.status_code == 200:
                texto_respuesta = respuesta.text
                print(Fore.GREEN + f"Subido a {opcion.capitalize()}: {texto_respuesta}")
            else:
                print(Fore.RED + f"Fallo al subir a {opcion.capitalize()}. Código de estado: {respuesta.status_code}")
    except Exception as e:
        print(Fore.RED + f"Ocurrió un error: {e}")

# Función para seleccionar el archivo usando termux-setup-storage
def seleccionar_archivo():
    try:
        # Ejecutar termux-setup-storage para permitir acceso a los archivos del dispositivo
        subprocess.run(["termux-setup-storage"])

        # Usar 'ls' para listar los archivos en el directorio seleccionado
        archivos_disponibles = subprocess.check_output(["ls", "-p", "/sdcard"]).decode("utf-8").strip().split('\n')

        # Mostrar los archivos disponibles al usuario
        print(Fore.YELLOW + "Archivos disponibles:")
        for idx, archivo in enumerate(archivos_disponibles, start=1):
            print(f"{idx}. {archivo}")

        # Solicitar al usuario que seleccione un archivo por número
        while True:
            try:
                seleccion = int(input(Fore.CYAN + "Selecciona el número del archivo que deseas subir: "))
                if 1 <= seleccion <= len(archivos_disponibles):
                    ruta_archivo = os.path.join("/sdcard", archivos_disponibles[seleccion - 1])
                    return ruta_archivo
                else:
                    print(Fore.RED + "Número fuera de rango. Introduce un número válido.")
            except ValueError:
                print(Fore.RED + "Entrada inválida. Introduce un número válido.")

    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"Error al acceder a los archivos: {e}")
        return None

# Función para mostrar el menú y manejar la opción seleccionada
def mostrar_menu():
    banner = Fore.CYAN + Style.BRIGHT + """
  ____       _   _   _       _          
 / ___| __ _| |_| \ | |_   _| |__   ___ 
| |  _ / _` | __|  \| | | | | '_ \ / _ \

| |_| | (_| | |_| |\  | |_| | |_) |  __/
 \____|\__,_|\__|_| \_|\__,_|_.__/ \___|
 _   _ ____  _                          
| | | |  _ \| |             _         ___               
| | | | |_) | |          / (_)          /                
| |_| |  _ <| |___      |         _    /                
 \___/|_| \_\_____|      \    \  (_)  / 
  By @AvastrOficial  / Version 0.0.1
"""
    while True:
        print(banner)
        print(Fore.YELLOW + """
    /\__/\  _
    • w •  /  1. Subir a Catbox""")
        print(Fore.YELLOW + """
    /\__/\  _
    • w •  /  2. Subir a Litterbox""")
        print(Fore.YELLOW + """
    /\__/\  _
    • w •  /  3. Salir""")

        eleccion = input(Fore.CYAN + "Selecciona una opción: ")

        if eleccion == '1':
            ruta_archivo = seleccionar_archivo()
            if ruta_archivo:
                cargar_archivo('catbox', ruta_archivo)
            else:
                print(Fore.RED + "No se seleccionó ningún archivo.")
        elif eleccion == '2':
            ruta_archivo = seleccionar_archivo()
            if ruta_archivo:
                expiracion = input(Fore.CYAN + "Introduce el tiempo de expiración (por ejemplo, 1h, 2d): ")
                cargar_archivo('litterbox', ruta_archivo, expiracion)
            else:
                print(Fore.RED + "No se seleccionó ningún archivo.")
        elif eleccion == '3':
            print(Fore.GREEN + "Saliendo de la herramienta.")
            break
        else:
            print(Fore.RED + "Opción inválida. Por favor, intenta nuevamente.")

if __name__ == "__main__":
    mostrar_menu()
