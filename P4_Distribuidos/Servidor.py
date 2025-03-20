import socket
import threading
import sys
lista_canciones = []
reloj_lamport = 0
id_servidor = None
pares = []  
lock_lista = threading.Lock()

def agregar_evento_cancion(timestamp, id_origen, cancion):
    global lista_canciones
    evento = (timestamp, id_origen, cancion)
    with lock_lista:
        if evento not in lista_canciones:
            lista_canciones.append(evento)
            lista_canciones.sort(key=lambda x: (x[0], x[1]))

def difundir_evento(timestamp, cancion):
    mensaje = f"SYNC {timestamp} {id_servidor} {cancion}"
    for par in pares:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(par)
            sock.sendall(mensaje.encode('utf-8'))
            sock.close()
        except Exception as e:
            print(f"Error al enviar a {par}: {e}")

def manejar_cliente(socket_cliente, direccion):
    global reloj_lamport
    print(f"Cliente conectado: {direccion}")
    try:
        while True:
            datos = socket_cliente.recv(1024).decode('utf-8').strip()
            if not datos:
                break
            # Comando para agregar canción
            if datos.upper().startswith("ADD "):
                cancion = datos[4:].strip()
                # Incrementa el reloj lógico local
                with lock_lista:
                    reloj_lamport += 1
                    tiempo_actual = reloj_lamport
                # Agrega el evento localmente
                agregar_evento_cancion(tiempo_actual, id_servidor, cancion)
                # Difunde el evento a los demás servidores
                difundir_evento(tiempo_actual, cancion)
                with lock_lista:
                    lista_str = ", ".join([e[2] for e in lista_canciones])
                respuesta = f"Canción agregada (timestamp {tiempo_actual}). Playlist: [{lista_str}]\n"
                socket_cliente.sendall(respuesta.encode('utf-8'))
            elif datos.upper() == "LIST":
                with lock_lista:
                    lista_str = ", ".join([e[2] for e in lista_canciones])
                respuesta = f"Playlist: [{lista_str}]\n"
                socket_cliente.sendall(respuesta.encode('utf-8'))
            else:
                socket_cliente.sendall("Comando no reconocido.\n".encode('utf-8'))
    except Exception as e:
        print(f"Error con cliente {direccion}: {e}")
    finally:
        socket_cliente.close()
        print(f"Cliente desconectado: {direccion}")

def escuchar_clientes(puerto_clientes):
    
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(('0.0.0.0', puerto_clientes))
    servidor.listen(5)
    print(f"Escuchando clientes en puerto {puerto_clientes}...")
    while True:
        socket_cliente, direccion = servidor.accept()
        threading.Thread(target=manejar_cliente, args=(socket_cliente, direccion), daemon=True).start()

def manejar_conexion_par(socket_par, direccion):

    global reloj_lamport
    try:
        datos = socket_par.recv(1024).decode('utf-8').strip()
        if datos.startswith("SYNC"):
            partes = datos.split(" ", 3)
            if len(partes) == 4:
                _, timestamp_str, id_origen_str, cancion = partes
                timestamp_recibido = int(timestamp_str)
                id_origen = int(id_origen_str)
                with lock_lista:
                    reloj_lamport = max(reloj_lamport, timestamp_recibido) + 1
                agregar_evento_cancion(timestamp_recibido, id_origen, cancion)
    except Exception as e:
        print(f"Error en conexión de par {direccion}: {e}")
    finally:
        socket_par.close()

def escuchar_pares(puerto_par):
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(('0.0.0.0', puerto_par))
    servidor.listen(5)
    print(f"Escuchando pares en puerto {puerto_par}...")
    while True:
        socket_par, direccion = servidor.accept()
        threading.Thread(target=manejar_conexion_par, args=(socket_par, direccion), daemon=True).start()

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Uso: python server.py <id_servidor> <puerto_clientes> <puerto_par> [host_par:puerto_par ...]")
        sys.exit(1)
    id_servidor = int(sys.argv[1])
    puerto_clientes = int(sys.argv[2])
    puerto_par = int(sys.argv[3])
    # Procesar los argumentos opcionales de pares (formato host:puerto_par)
    if len(sys.argv) > 4:
        for arg in sys.argv[4:]:
            try:
                host, puerto_str = arg.split(":")
                pares.append((host, int(puerto_str)))
            except:
                print(f"Par {arg} inválido. Formato esperado host:puerto")
    print(f"Iniciando servidor {id_servidor} con puerto_clientes {puerto_clientes} y puerto_par {puerto_par}. Pares: {pares}")
    # Inicia hilos para los sockets de clientes y otros servidores
    threading.Thread(target=escuchar_clientes, args=(puerto_clientes,), daemon=True).start()
    threading.Thread(target=escuchar_pares, args=(puerto_par,), daemon=True).start()

    # Mantiene el hilo principal activo
    while True:
        pass
