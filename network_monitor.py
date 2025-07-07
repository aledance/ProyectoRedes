# network_monitor.py
import subprocess
import re

def get_latency_and_hops(destination):
    """Ejecuta ping y traceroute para obtener latencia y saltos."""
    latency = get_avg_latency(destination)
    hops = get_hops_count(destination)
    return latency, hops

def get_avg_latency(destination):
    """Ejecuta 4 pings y extrae la latencia promedio."""
    command = ['ping', '-c', '4', destination] # [cite: 64]
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
        # Búsqueda de la línea de estadísticas (funciona en Linux)
        match = re.search(r'rtt min/avg/max/mdev = [\d.]+/([\d.]+)/[\d.]+/[\d.]+ ms', output)
        if match:
            return float(match.group(1)) # Retorna el valor de latencia promedio [cite: 67]
    except subprocess.CalledProcessError as e:
        # Esto ocurre si el ping falla (host inalcanzable)
        print(f"Error al hacer ping a {destination}: {e.output}")
    except Exception as e:
        print(f"Un error inesperado ocurrió: {e}")
    return None # Retorna None si no se puede obtener la latencia

def get_hops_count(destination):
    """Ejecuta traceroute y cuenta los saltos."""
    command = ['traceroute', '-n', destination]
    try:
        # Usamos check_output para capturar la salida
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
        # Contamos las líneas de saltos (líneas que empiezan con un número)
        hops = len(re.findall(r'^\s*\d+', output, re.MULTILINE))
        return hops
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar traceroute a {destination}: {e.output}")
    except Exception as e:
        print(f"Un error inesperado ocurrió: {e}")
    return None