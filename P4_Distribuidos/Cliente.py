import socket
import sys

def iniciar_cliente(host_servidor, puerto_clientes):
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        cliente.connect((host_servidor, puerto_clientes))
        print(f"Conectado a la sala en {host_servidor}:{puerto_clientes}.")
        print("Comandos disponibles:\n  ADD <canción>\n  LIST\n  EXIT")
        while True:
            comando = input("Ingresa comando: ")
            if comando.upper() == "EXIT":
                break
            cliente.sendall(comando.encode('utf-8'))
            respuesta = cliente.recv(4096).decode('utf-8')
            print("Respuesta del servidor:", respuesta)
    except Exception as e:
        print("Error:", e)
    finally:
        cliente.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python client.py <host_servidor> <puerto_clientes>")
        sys.exit(1)
    host_servidor = sys.argv[1]
    puerto_clientes = int(sys.argv[2])
    iniciar_cliente(host_servidor, puerto_clientes)
