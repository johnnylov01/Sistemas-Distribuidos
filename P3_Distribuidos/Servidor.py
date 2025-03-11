import socket
import os
import shutil
import threading
import queue

# Configuración inicial
directorio_base = "C:\\Users\\pande\\Documents\\PruebasRedes"
os.makedirs(directorio_base, exist_ok=True)
socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
direccion = ('localhost', 4000)
socket_servidor.bind(direccion)

clientes_dirs = {}
operaciones_queue = queue.Queue()
# Lock para proteger el acceso a los recursos compartidos
lock = threading.Lock()

def get_client_dir(dir_cliente):
    with lock:
        if dir_cliente not in clientes_dirs:
            clientes_dirs[dir_cliente] = directorio_base
        return clientes_dirs[dir_cliente]

def set_client_dir(dir_cliente, nueva_ruta):
    with lock:
        clientes_dirs[dir_cliente] = nueva_ruta

def operaciones(opc, args, dir_cliente, datos=None):
    try:
        current_dir = get_client_dir(dir_cliente)
        
        if opc == "1":  # Crear archivo
            ruta = os.path.join(current_dir, args[0])
            with open(ruta, 'w') as f:
                f.write("")
            return "Acuse: Archivo creado con éxito!"
        
        elif opc == "2":  # Recibir archivo
            nombre_archivo = args[0]
            ruta = os.path.join(current_dir, nombre_archivo)
            with open(ruta, "wb") as archivo:
                while True:
                    datos, cliente = socket_servidor.recvfrom(1024)
                    if datos == b"EOF":
                        break
                    archivo.write(datos)
            return f"Acuse: Archivo '{nombre_archivo}' recibido y guardado con éxito!"
        
        elif opc == "3":  # Renombrar archivo
            nombre_antiguo, nombre_nuevo = args
            os.rename(os.path.join(current_dir, nombre_antiguo), os.path.join(current_dir, nombre_nuevo))
            return "Acuse: Archivo renombrado con éxito!"
        
        elif opc == "4":  # Eliminar archivo
            ruta_archivo = os.path.join(current_dir, args[0])
            if os.path.exists(ruta_archivo):
                os.remove(ruta_archivo)
                return f"Acuse: Archivo '{args[0]}' eliminado correctamente!"
            else:
                return f"Error: Archivo '{args[0]}' no encontrado"
                        
        elif opc == "5" or opc == "5_listar":  # Descargar archivo o listar archivos
            if opc == "5_listar":  # Listar archivos
                archivos = os.listdir(current_dir)
                return "\n".join(archivos) or "Directorio vacío"
            else:  # Descargar archivo
                ruta_archivo = os.path.join(current_dir, args[0])
                if not os.path.exists(ruta_archivo):
                    return "ERROR: Archivo no encontrado"
                
                # Enviar señal de que el archivo existe
                socket_servidor.sendto("Archivo encontrado".encode(), dir_cliente)
                
                # Esperar señal READY del cliente
                while True:
                    datos, cliente = socket_servidor.recvfrom(1024)
                    if datos == b"READY" and cliente == dir_cliente:
                        with open(ruta_archivo, "rb") as archivo:
                            while chunk := archivo.read(1024):
                                socket_servidor.sendto(chunk, dir_cliente)
                                # Esperar siguiente señal READY
                                datos, cliente = socket_servidor.recvfrom(1024)
                                if datos != b"READY" or cliente != dir_cliente:
                                    break
                        socket_servidor.sendto(b"EOF", dir_cliente)
                        break
                return "Archivo enviado correctamente"
        
        elif opc == "6":  # Crear carpeta
            ruta_carpeta = os.path.join(current_dir, args[0])
            os.makedirs(ruta_carpeta, exist_ok=True)
            return "Acuse: Carpeta creada con éxito!"
        
        elif opc == "7":  # Cambiar de carpeta
            nueva_ruta = os.path.join(current_dir, args[0])
            if args[0] == "..":
                nueva_ruta = os.path.abspath(os.path.join(current_dir, ".."))
            if os.path.isdir(nueva_ruta):
                archivos = os.listdir(nueva_ruta) or ["Directorio vacío"]
                set_client_dir(dir_cliente, nueva_ruta)
                return f"Acuse: Cambiado al directorio {nueva_ruta}\nContenido:\n" + "\n".join(archivos)
            return "Error: Carpeta no encontrada"
        
        elif opc == "8":  # Eliminar carpeta
            ruta_carpeta = os.path.join(current_dir, args[0])
            if os.path.exists(ruta_carpeta) and os.path.isdir(ruta_carpeta):
                shutil.rmtree(ruta_carpeta)
                return f"Acuse: Carpeta '{args[0]}' eliminada con éxito!"
            else:
                return f"Error: Carpeta '{args[0]}' no encontrada"
        
        elif opc == "9":  # Renombrar carpeta
            nombre_antiguo, nombre_nuevo = args
            os.rename(os.path.join(current_dir, nombre_antiguo), os.path.join(current_dir, nombre_nuevo))
            return "Acuse: Carpeta renombrada con éxito!"
        
        elif opc == "cerrar_servidor":
            return "Acuse: Servidor cerrando..."
        
        else:
            return "Comando inválido" 
    except Exception as e:
        return f"Error: {str(e)}"

def procesar_cola():
    while True:
        try:
            # Esperar por nueva operación en la cola
            item = operaciones_queue.get()
            if item is None:  # Señal para terminar
                break
                
            opc, args, dir_cliente, datos = item
            
            # Ejecutar operación
            respuesta = operaciones(opc, args, dir_cliente, datos)
            
            # Enviar respuesta
            socket_servidor.sendto(respuesta.encode(), dir_cliente)
            
            # Marcar tarea como completada
            operaciones_queue.task_done()
        except Exception as e:
            print(f"Error en el procesador de cola: {str(e)}")

def manejar_cliente():
    while True:
        try:
            datos, dir_cliente = socket_servidor.recvfrom(1024)
            mensaje = datos.decode()
            partes = mensaje.split("|||")
            opc = partes[0]
            args = partes[1:] if len(partes) > 1 else []

            if opc == "cerrar_servidor":
                socket_servidor.sendto("Servidor cerrando...".encode(), dir_cliente)
                # Señal para terminar los hilos
                operaciones_queue.put(None)
                break
            
            # Añadir operación a la cola
            operaciones_queue.put((opc, args, dir_cliente, datos))
            
        except Exception as e:
            print(f"Error al recibir mensaje: {str(e)}")

# Iniciar el hilo procesador de cola
hilo_procesador = threading.Thread(target=procesar_cola, daemon=True)
hilo_procesador.start()

# Iniciar el hilo manejador de clientes
hilo_manejador = threading.Thread(target=manejar_cliente, daemon=True)
hilo_manejador.start()

print(f"Servidor iniciado en {direccion}")
print(f"Directorio base: {directorio_base}")
print("Esperando conexiones de clientes...")

try:
    # Mantener el hilo principal vivo
    hilo_manejador.join()
finally:
    socket_servidor.close()
    print("Servidor cerrado.")