# ProyectoRedes 🥅🌐

A continuación, se encuentra una guía detallada paso a paso para ser desarrollada en Linux Mint (o cualquier sub-distro de Debian Linux, ej: Ubuntu).
Para el proyecto de monitoreo de red utilizando Telegram y MQTT. Este proyecto integra un bot de Telegram que permite a los usuarios monitorear la conectividad de red mediante comandos específicos, y utiliza MQTT para enviar mensajes y alertas.

## **Guía para el Proyecto Final: Monitoreo de Red con Telegram y MQTT**
Esta guía está estructurada para cubrir todos los objetivos del proyecto[cite: 9, 11], desde la configuración inicial hasta la implementación de cada módulo y las pruebas finales.

-----

### **Parte 1: Preparación del Entorno** 🛠️
Antes de replicar el presente proyecto, es crucial preparar el entorno de ejecucion. Esto asegura que el proyecto sea reproducible y que no se comparta accidentalmente información sensible publicamente.

#### **1.1. Estructura de Carpetas del Proyecto**
La estructura del proyecto tiene la siguiente forma:
```
proyecto-redes/
├── .gitignore
├── config.py             # Para guardar tokens y configuraciones
├── main_bot.py           # El código principal del bot (evolución de tu bot.py)
├── network_monitor.py    # Funciones para ejecutar ping y traceroute
├── mqtt_client.py        # Lógica para conectar y publicar en MQTT
├── requirements.txt      # Lista de librerías de Python necesarias
└── README.md             # Descripción del proyecto
```

#### **1.2. Entorno Virtual y Dependencias**
Se usa un entorno virtual en Python (venv), para aislar las librerías del proyecto.

1.  **Abre una terminal** en tu carpeta `proyecto-redes`.
    Este archivo le permite a otros (o desde otra maquina) instalar las mismas dependencias fácilmente.

2. Creacion del entorno virtual:
```bash
python -m venv venv
```

3. activacion del entorno virtual:
```bash
# En Linux
source venv/bin/activate
```

4. instalacion de las dependencias (encontradas en el archivo `requirements.txt`):
```bash
pip install -r requirements.txt
```

5. (opcional) para detener y salirse del entorno virtual, luego de la demostracion del proyecto, puedes usar el comando:
```bash
deactivate
```

#### **1.3. Control de Versiones con Git**
Dentro del archivo .gitignore, se encuentran los archivos y carpetas que no deben subirse al repositorio, como el entorno virtual `venv`, el cual debe ser creado al clonar el repositorio, descrito en la parte 3 de esta guia. Y el archivo de configuración con los tokens `config.py` (se encuentra un archivo `config_example.py` que muestra como debe estar estructurado).

#### **1.4. Configuracion del Telegram Bot** 🤖
1. Crear un bot en Telegram:
   - Buscar el bot "BotFather" en Telegram.
   - Enviar el comando `/newbot` y seguir las instrucciones para crear un nuevo bot.
   - Guardar el token del bot que se te proporcionará.  
2. Configurar el bot en el proyecto:
   - Editar el archivo `config.py` y agregar el token del bot:
   - una vez teniendo el token, agregarlo al siguiente link y abrelo en un navegador web para recuperar el ID de chat:
    ```
    https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getMe
    # ejemplo: https://api.telegram.org/bot5555555555:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/getMe
    ```
      - copiar el `id` del chat que se encuentra dentro del json, y agregarlo al archivo `config.py`:


-----
### **Parte 2: Configuración del Broker MQTT (Mosquitto)** 💌
El proyecto requiere de un broker MQTT local, se utilizará este Broker, el cual es Open Source.

1.  **Instala Mosquitto:**
    ```bash
    sudo apt update
    sudo apt install mosquitto mosquitto-clients -y
    ```
2.  **Configura el Broker:** Edita el archivo de configuración.
    ```bash
    sudo nano /etc/mosquitto/mosquitto.conf
    # sudo vim /etc/mosquitto/mosquitto.conf
    ```
3.  **Añade las siguientes líneas** para permitir conexiones anónimas para las pruebas iniciales:
    ```conf
    listener 1883
    allow_anonymous true
    ```
4.  **Inicia y habilita el servicio Mosquitto:**
    ```bash
    sudo systemctl start mosquitto
    sudo systemctl enable mosquitto
    ```
5.  **Verifica que está funcionando:**
    ```bash
    sudo systemctl status mosquitto
    ```
    Deberías ver un estado `active (running)`
6.  **Configura el Firewall:** Si se tiene el firewall `ufw` activado, permite el tráfico en el puerto 1883.
    ```bash
    sudo ufw allow 1883/tcp
    ```

-----
### **Parte 3: Desarrollo del Código Python (Módulos)** 🐍
Aqui se tiene una explicacion breve de los archivos principales segun la estructura de archivos que definimos.

#### **3.1. Módulo de Configuración (`config.py`)**
Crea el archivo `config.py` para centralizar tus variables. **Recuerda no subir este archivo a Git**, ya se encuentra en el `.gitignore`.
```python
# config.py

# --- Telegram Bot ---
BOT_TOKEN = '7000000002:AAHv-PxxxxxxxxxxxoyAxxxxxxxxxxxxxxc' # Tu token
ADMIN_CHAT_ID = '1000000004' # Tu ID de chat para recibir alertas

# --- MQTT Broker ---
MQTT_BROKER_HOST = 'localhost' # O la IP de tu servidor Mosquitto
MQTT_BROKER_PORT = 1883
[cite_start]MQTT_TOPIC = 'mensaje_grupo' # Tópico especificado en el proyecto [cite: 16, 78]
```

#### **3.2. Módulo del Cliente MQTT (`mqtt_client.py`)**
Este módulo se encargará de toda la comunicación con Mosquitto, usando la librería `paho-mqtt`

#### **3.3. Módulo de Monitoreo de Red (`network_monitor.py`)**
Aquí se implementa la ejecución de los comandos `ping` y `traceroute`
> **Nota sobre `traceroute`**: Puede que necesites instalarlo (`sudo apt install traceroute`) y, en algunos sistemas, puede requerir privilegios de superusuario.

#### **3.4. Módulo Principal del Bot (`main_bot.py`)**
Este es el cerebro del proyecto. Aqui se integra todo y maneja la interacción con el usuario a través de Telegram. Se utiliza la librería `telepot` para interactuar con la API de Telegram. 

-----
### **Parte 4: Pruebas y Visualización** 🧪
Esta es la fase de evaluación, donde compruebas que todo funciona como se espera[cite: 85, 98].

1.  **Ejecuta tu bot:** 👩‍💻 Desde tu terminal con el entorno virtual activado, corre:
    ```bash
    python main_bot.py
    ```
2.  **Interactúa con el Bot en Telegram:**
      * Envía `/start` para ver los comandos.
      * Envía `/monitor google.com` para probar el monitoreo único.
      * Envía `/start_alert 8.8.8.8` para iniciar las alertas.
      * Envía `/stop_alert` para detenerlas.
3.  **Visualiza en MQTT Explorer:**
      * Descarga e instala [MQTT Explorer](http://mqtt-explorer.com/).
      * [cite\_start]Ábrelo y crea una nueva conexión[cite: 352].
      * **Host**: `localhost`, **Port**: `1883`. No necesitas usuario/clave con la configuración actual.
      * Conéctate.
      * [cite\_start]Cada vez que ejecutes `/monitor <destino>`, verás un nuevo mensaje en el tópico `mensaje_grupo`[cite: 353].
      * [cite\_start]**Para los gráficos[cite: 17, 83, 103]:**
          * Haz clic en el tópico `mensaje_grupo`.
          * En la sección "History", verás los valores de `latencia_promedio` y `saltos`.
          * Puedes hacer clic en el ícono de gráfico al lado de cada valor para visualizarlos como una serie de tiempo.

### **Issues y Recomendaciones Finales (WIP👷‍♀️⚒⚒)**
  * [ ] FIX 🔨: `Fallo al publicar en el tópico 'mensaje_grupo'`
    - mensaje en main_bot.py en modo escucha, al publicar en el topico de MQTT/MQTT Explorer , una vez empezadas las alertas (estando `/start alert 8.8.8.8` activo en bot de Telegram).
-----
  Otros detalles menores que se pueden mejorar en el proyecto:
  * [ ] **Portabilidad** revision de como se puede dockerizar el proyecto en el apartado de MQTT, para que sea portable y se pueda ejecutar en cualquier sistema operativo como Windows.
  * [ ] [cite\_start]**Seguridad:** Para un despliegue final, se debe de proteger el broker MQTT con usuario y contraseña como se describe en el `laboratorio-mqtt.pdf` [cite: 93, 280-291]. Se debe adaptar el `mqtt_client.py` para incluir el usuario y la contraseña.
  * [ ] **Manejo de Errores:** El código proporcionado tiene un manejo básico de errores. [cite\_start] se puede expandir para ser más robusto, por ejemplo; reintentar la conexión al broker MQTT si falla[cite: 94].
  * [ ] **Documentación:** Asegurarse que el código esté bien documentado y que el README.md termine de explicar claramente cómo configurar y ejecutar el proyecto.

### Useful libraries's docs partially applied in this project:
- telegram bots docs: https://core.telegram.org/bots/api
- telepot: https://telepot.readthedocs.io/en/latest/