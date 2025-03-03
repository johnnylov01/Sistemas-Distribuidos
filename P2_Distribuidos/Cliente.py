import socket
import os

socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip = "localhost"
puerto = 4000
direccion = (ip, puerto)
timeout = 60 # 60 segundos
socket_cliente.settimeout(timeout)

def env_recibir(comando, args):
    if args is None:
        args = []
    mensaje = f"{comando}|||" + "|||".join(args)
    intentos = 0
    while intentos < 3:
        try:
            socket_cliente.sendto(mensaje.encode(), direccion)
            respuesta, _ = socket_cliente.recvfrom(1024)
            return respuesta.decode()
        except socket.timeout:
            intentos += 1
            print(f"Reintentando {intentos}...")
    return "No se ha podido establecer la conexión"

def enviar_archivo(ruta):
    try:
        if not os.path.isfile(ruta):
            print("Error: La ruta proporcionada no es válida.")
            return        
        nombre_archivo = os.path.basename(ruta)
        tamano_total = os.path.getsize(ruta)
        paquetes_enviados = 0
        bytes_enviados = 0
        socket_cliente.sendto(f"2|||{nombre_archivo}".encode(), direccion)

        with open(ruta, "rb") as archivo:
            while (datos := archivo.read(1024)):
                socket_cliente.sendto(datos, direccion)
                bytes_enviados += len(datos)
                paquetes_enviados += 1
                porcentaje = (bytes_enviados / tamano_total) * 100

                # Mostrar progreso
                print(f"\rEnviando archivo... {porcentaje:.2f}% ({paquetes_enviados} paquetes enviados)", end="")

        # Enviar señal de finalización
        socket_cliente.sendto(b"EOF", direccion)
        print("\nArchivo enviado correctamente.")
    except Exception as e:
        print(f"Error al enviar el archivo: {str(e)}")


def mostrar_menu_principal(extra_opcion=None):
    """Muestra el menú principal con opciones adicionales si las hay."""
    print("\n***** Bienvenido a Daraiv *****")
    print("1. Crear archivo\n2. Enviar archivo\n3. Renombrar archivo\n4. Eliminar archivo")
    print("5. Descargar archivo\n6. Crear carpeta\n7. Abrir carpeta\n8. Eliminar carpeta\n9. Renombrar carpeta\n10. Salir")
    if extra_opcion:
        print(extra_opcion)

def descargar_archivo(nombrearchivo):
    """Solicita un archivo al servidor y lo descarga."""
    try:
        # Primero verificamos si el archivo existe
        respuesta = env_recibir("5", [nombrearchivo])
        if respuesta.startswith("ERROR"):
            print(respuesta)
            return

        # Comenzamos la descarga
        with open(nombrearchivo, "wb") as archivo:
            bytes_recibidos = 0
            while True:
                try:
                    socket_cliente.sendto(b"READY", direccion) 
                    datos, _ = socket_cliente.recvfrom(1024)
                    
                    if datos == b"EOF":
                        print("\nDescarga completada.")
                        break
                        
                    archivo.write(datos)
                    bytes_recibidos += len(datos)
                    print(f"\rRecibidos {bytes_recibidos} bytes", end="")
                    
                except socket.timeout:
                    print("\nTimeout durante la descarga. Reintentando...")
                    continue
                    
    except Exception as e:
        print(f"Error al descargar el archivo: {str(e)}")
        if os.path.exists(nombrearchivo):
            os.remove(nombrearchivo)  # Limpiamos el archivo parcial en caso de error

def abrir_carpeta():
    """Navega dentro de una carpeta y muestra un submenú."""
    while True:
        mostrar_menu_principal("11. Salir de la carpeta")
        opcion = input("Ingrese la opción deseada: ").strip()
        
        if opcion == "1":
            nombre_archivo = input("Ingrese el nombre del archivo: ").strip()
            print(env_recibir("1", [nombre_archivo]))
        elif opcion == "2":
            ruta_archivo = input("Ingrese la ruta completa del archivo a enviar: ").strip()
            enviar_archivo(ruta_archivo)
        elif opcion == "3":
            nombre_antiguo = input("Ingrese el nombre del archivo a renombrar: ").strip()
            nombre_nuevo = input("Ingrese el nuevo nombre del archivo: ").strip()
            print(env_recibir("3", [nombre_antiguo, nombre_nuevo]))
        elif opcion == "4":
            nombre_archivo = input("Ingrese el nombre del archivo a eliminar: ").strip()
            print(env_recibir("4", [nombre_archivo]))
        elif opcion == "5":
            lista_archivos = env_recibir("5_listar", None)
            print("Archivos disponibles:")
            print(lista_archivos)
            nombre_archivo = input("Ingrese el nombre del archivo a descargar: ").strip()
            descargar_archivo(nombre_archivo)
        elif opcion == "6":
            nombre_carpeta = input("Ingrese el nombre de la carpeta a crear: ").strip()
            print(env_recibir("6", [nombre_carpeta]))
        elif opcion == "7":
            nombre_carpeta = input("Ingrese el nombre de la carpeta: ").strip()
            respuesta = env_recibir("7", [nombre_carpeta])
            print(respuesta)
        elif opcion == "8":
            nombre_carpeta = input("Ingrese el nombre de la carpeta a eliminar: ").strip()
            print(env_recibir("8", [nombre_carpeta]))
        elif opcion == "9":
            nombre_antiguo = input("Ingrese el nombre de la carpeta a renombrar: ").strip()
            nombre_nuevo = input("Ingrese el nuevo nombre de la carpeta: ").strip()
            print(env_recibir("9", [nombre_antiguo, nombre_nuevo]))
        elif opcion == "10":
            print("Saliendo del programa...")
            socket_cliente.close()  
            exit()
        elif opcion == "11":
            print(env_recibir("7", [".."])) 
            break
        else:
            print("Opción no válida")

# Programa principal
try:
    while True:
        mostrar_menu_principal()
        opcion = input("Ingrese la opción deseada: ").strip()
        
        if opcion == "1":
            nombre_archivo = input("Ingrese el nombre del archivo: ").strip()
            print(env_recibir("1", [nombre_archivo]))
        elif opcion == "2":
            ruta_archivo = input("Ingrese la ruta completa del archivo a enviar: ").strip()
            enviar_archivo(ruta_archivo)
        elif opcion == "3":
            nombre_antiguo = input("Ingrese el nombre del archivo a renombrar: ").strip()
            nombre_nuevo = input("Ingrese el nuevo nombre del archivo: ").strip()
            print(env_recibir("3", [nombre_antiguo, nombre_nuevo]))
        elif opcion == "4":
            nombre_archivo = input("Ingrese el nombre del archivo a eliminar: ").strip()
            print(env_recibir("4", [nombre_archivo]))
        elif opcion == "5":
            lista_archivos = env_recibir("5_listar", None)
            print("Archivos disponibles:")
            print(lista_archivos)
            nombre_archivo = input("Ingrese el nombre del archivo a descargar: ").strip()
            descargar_archivo(nombre_archivo)
        elif opcion == "6":
            nombre_carpeta = input("Ingrese el nombre de la carpeta a crear: ").strip()
            print(env_recibir("6", [nombre_carpeta]))
        elif opcion == "7":
            nombre_carpeta = input("Ingrese el nombre de la carpeta: ").strip()
            respuesta = env_recibir("7", [nombre_carpeta])
            print(respuesta)
            abrir_carpeta()
        elif opcion == "8":
            nombre_carpeta = input("Ingrese el nombre de la carpeta a eliminar: ").strip()
            print(env_recibir("8", [nombre_carpeta]))
        elif opcion == "9":
            nombre_antiguo = input("Ingrese el nombre de la carpeta a renombrar: ").strip()
            nombre_nuevo = input("Ingrese el nuevo nombre de la carpeta: ").strip()
            print(env_recibir("9", [nombre_antiguo, nombre_nuevo]))
        elif opcion == "10":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida")
finally:
    socket_cliente.close() 