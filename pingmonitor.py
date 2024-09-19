import os
import time
from datetime import datetime

def ping_ip(ip_address):
    # Comando de ping para Windows (envía 1 ping y espera 1 segundo)
    response = os.system(f"ping -n 1 -w 1000 {ip_address} > NUL 2>&1")
    return response == 0

def log_event(event, count_disconnections, last_disconnection, last_reconnection):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{datetime.now()}: {event}")
    print("\nTabla de Estado:")
    print(f"{'Total desconexiones:':<30}{count_disconnections}")
    print(f"{'Hora de la última desconexión:':<30}{last_disconnection}")
    print(f"{'Hora de la última reconexión:':<30}{last_reconnection}\n")

def monitor_ip(ip_address):
    was_connected = True
    count_disconnections = 0
    last_disconnection = "N/A"
    last_reconnection = "N/A"

    while True:
        if ping_ip(ip_address):
            if not was_connected:
                last_reconnection = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_event(f"Reconexión con {ip_address}", count_disconnections, last_disconnection, last_reconnection)
                was_connected = True
            
            # Mostrar "Conexión correcta..." con puntos variables
            dots = "." * (datetime.now().second % 3 + 1)
            print(f"\rConexión correcta{dots}", end="")
        else:
            if was_connected:
                last_disconnection = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                count_disconnections += 1
                log_event(f"Desconexión de {ip_address}", count_disconnections, last_disconnection, last_reconnection)
                was_connected = False
        
        time.sleep(1)  # Espera 1 segundo antes de hacer el siguiente ping

if __name__ == "__main__":
    ip_address = "172.16.1.105"  # Reemplaza con la dirección IP que deseas monitorear
    monitor_ip(ip_address)
