# main_bot.py
import time
import telepot
import threading
from config import BOT_TOKEN, ADMIN_CHAT_ID
from network_monitor import get_latency_and_hops, get_avg_latency
from mqtt_client import connect_mqtt, publish_metrics

# --- Variables Globales para el monitoreo recurrente ---
monitoring_thread = None
stop_monitoring_event = threading.Event()

# --- Cliente MQTT Global ---
mqtt_client = connect_mqtt()

def one_time_monitor(chat_id, destination):
    """Función para el comando /monitor <destino>."""
    bot.sendMessage(chat_id, f"Iniciando monitoreo para {destination}...")
    
    latency, hops = get_latency_and_hops(destination)
    
    if latency is not None and hops is not None:
        response = (f"Resultados para {destination}:\n"
                    f"- Latencia Promedio: {latency} ms\n"
                    f"- Saltos: {hops}")
        bot.sendMessage(chat_id, response) # [cite: 101]
        
        # Publicar en MQTT [cite: 16, 78]
        publish_metrics(mqtt_client, latency, hops)
    else:
        bot.sendMessage(chat_id, f"No se pudo obtener la información para {destination}. "
                                 f"Verifica que el destino es alcanzable.")

def recurring_monitor_task(destination):
    """Tarea que se ejecuta en un hilo para el monitoreo de alertas."""
    print(f"Iniciado monitoreo recurrente para {destination}.")
    
    while not stop_monitoring_event.is_set():
        latency = get_avg_latency(destination)
        
        if latency is None:
            # Si la latencia es None, el host está inalcanzable
            alert_message = f"🚨 ¡ALERTA! El host {destination} está inalcanzable. 🚨"
            bot.sendMessage(ADMIN_CHAT_ID, alert_message) # [cite: 70, 82, 101]
            print(alert_message)
        
        # Espera 10 segundos antes de la siguiente verificación. 
        # El proyecto recomienda un retardo > 5 segundos[cite: 65, 96].
        time.sleep(10)
        
    print(f"Detenido el monitoreo recurrente para {destination}.")

def handle(msg):
    global monitoring_thread
    content_type, chat_type, chat_id = telepot.glance(msg)
    
    if content_type != 'text':
        return

    command_text = msg['text']
    print(f"Recibido de {chat_id}: {command_text}")

    parts = command_text.split()
    command = parts[0]
    args = parts[1:]

    if command == '/start':
        bot.sendMessage(chat_id, "¡Hola! Soy tu bot de monitoreo de red.\n\n"
                                 "Comandos disponibles:\n"
                                 "/monitor <destino> - Mide latencia y saltos una vez.\n"
                                 "/start_alert <destino> - Inicia el monitoreo de caídas.\n"
                                 "/stop_alert - Detiene el monitoreo de caídas.")

    elif command == '/monitor' and args: # [cite: 99]
        destination = args[0]
        one_time_monitor(chat_id, destination)

    elif command == '/start_alert' and args: # [cite: 69]
        if monitoring_thread and monitoring_thread.is_alive():
            bot.sendMessage(chat_id, "Ya hay un monitoreo de alertas en ejecución.")
            return
        
        destination = args[0]
        stop_monitoring_event.clear()
        monitoring_thread = threading.Thread(target=recurring_monitor_task, args=(destination,))
        monitoring_thread.start()
        bot.sendMessage(chat_id, f"✅ Monitoreo de alertas iniciado para {destination}. "
                                 f"Se te notificará si se vuelve inalcanzable.")

    elif command == '/stop_alert': # [cite: 73, 105]
        if monitoring_thread and monitoring_thread.is_alive():
            stop_monitoring_event.set()
            bot.sendMessage(chat_id, "🛑 Deteniendo el monitoreo de alertas...")
        else:
            bot.sendMessage(chat_id, "No hay ningún monitoreo de alertas activo para detener.")

    else:
        bot.sendMessage(chat_id, "Comando no reconocido. Escribe /start para ver las opciones.")

# --- Bucle Principal ---
bot = telepot.Bot(BOT_TOKEN)
bot.message_loop(handle)
print('Bot en línea y escuchando...')

# Mantener el programa en ejecución
while 1:
    time.sleep(10)