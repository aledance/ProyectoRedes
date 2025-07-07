# mqtt_client.py
import paho.mqtt.client as mqtt
import json
from config import MQTT_BROKER_HOST, MQTT_BROKER_PORT, MQTT_TOPIC

def connect_mqtt():
    """Crea y retorna un cliente MQTT conectado."""
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
    try:
        client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)
        print("Conectado al broker MQTT exitosamente.")
        return client
    except Exception as e:
        print(f"Error al conectar al broker MQTT: {e}")
        return None

def publish_metrics(client, latency, hops):
    """Publica la latencia y los saltos en el tópico MQTT."""
    if client is None:
        print("El cliente MQTT no está conectado. No se puede publicar.")
        return

    # Usamos JSON para un formato estructurado
    payload = json.dumps({
        "latencia_promedio": latency,
        "saltos": hops
    })
    
    result = client.publish(MQTT_TOPIC, payload)
    # Verificamos si la publicación fue exitosa
    if result[0] == 0:
        print(f"Publicado en '{MQTT_TOPIC}': {payload}")
    else:
        print(f"Fallo al publicar en el tópico '{MQTT_TOPIC}'")