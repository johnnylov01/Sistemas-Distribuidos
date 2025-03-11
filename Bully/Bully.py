import random
import time

def enviar_mensaje(remitente, receptor, mensaje, tiempo_propagacion):
    print(f"Proceso {remitente} envía '{mensaje}' a Proceso {receptor}")
    time.sleep(tiempo_propagacion)  # tiempo de propagación del mensaje

def algoritmo_bully(procesos, coordinador, tiempo_propagacion, tiempo_tratamiento):
    n = len(procesos)
    for i in range(n):
        if procesos[i] > coordinador:
            enviar_mensaje(coordinador, procesos[i], "Elección", tiempo_propagacion)
            time.sleep(tiempo_tratamiento)  
            respuesta = random.choice([True, False])  # Simula si el proceso responde o no
            if respuesta:
                print(f"Proceso {procesos[i]} responde a Proceso {coordinador}")
                algoritmo_bully(procesos, procesos[i], tiempo_propagacion, tiempo_tratamiento)
                return
    print(f"Proceso {coordinador} es el nuevo coordinador")

def main():
    procesos = [1, 2, 3, 4, 5, 6, 7, 8]
    coordinador = max(procesos)
    tiempo_propagacion = 1  
    tiempo_tratamiento = 1  

    print(f"Proceso {coordinador} es el coordinador inicial")
    
    #caída del coordinador
    time.sleep(2)
    print(f"Proceso {coordinador} ha fallado")
    procesos.remove(coordinador)
    
    # Inicia una nueva elección
    nuevo_coordinador = random.choice(procesos)
    print(f"Proceso {nuevo_coordinador} inicia una nueva elección")
    algoritmo_bully(procesos, nuevo_coordinador, tiempo_propagacion, tiempo_tratamiento)

if __name__ == "__main__":
    main()