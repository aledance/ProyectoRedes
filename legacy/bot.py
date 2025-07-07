import time
import telepot
import datetime

TOKEN = '7356030162:AAHv-PITrYkqtT6i0oyAU1mQUBwkfjEUHdc'
chat_id = '1305870044'

def metrica(chat_id):
    resultado=(f"fecha y hora {fecha_y_hora()}\n")
    bot.sendMessage(chat_id, resultado)
    save_event_file(resultado)
    return

def fecha_y_hora():
    fecha = datetime.date.today()
    hora = datetime.datetime.now()
    return str (fecha) + ' ' + str(hora.hour) + ':' + str(hora.minute) + ':' + str(hora.second)

def save_event_file(res):
    with open("evento", "a") as f:
        f.write(res + "\n")
    return

def handle(msg):
    #bot.sendMessage(chat_id, "conectado")
    content_type, chat_type, chat_id = telepot.glance(msg)
    #print(content_type, chat_type, chat_id)
    print(msg['text'])
    if content_type == 'text':
        if msg['text'] == '/metrica':
            metrica(chat_id)
    return

###### MAIN ######
bot = telepot.Bot(TOKEN)
bot.message_loop(handle)
print('Leyendo...')

#Keep the program running.
while 1:
    try:
        #check_event_file()
        time.sleep(10)
    except Exception as e:
        print ('error', e, 'reconectando...')
        time.sleep(10)
        