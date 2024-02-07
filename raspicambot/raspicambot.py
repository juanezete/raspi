# Se importan las clases necesarias para la PiCamera
from picamera.array import PiRGBArray
from picamera import PiCamera
# Clases para el manejo del bot de Telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
# Clase necesaria para la implementación del timer para la toma continua de fotos
from threading import Timer

# Se inicializa la cámara y se configura
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
camera.rotation = 0
camera.hflip = True
rawCapture = PiRGBArray(camera, size=(640, 480))

# RToken del Bot de Telegram
TOKEN = '6829164131:AAGXo6UmiBxvnoERGIW9ibV0CQP1RCeWZW0'

# Flags para la toma periódica de fotos
fotos_intervalo_flag = True
msg_flag = True

# Función de mensaje de bienvenida y lista de comandos disponibles
def start(update: Update, context: CallbackContext):
    update.message.reply_text('Hola! Soy RaspiCamBot \U0001F916. Aquí está la lista de comandos disponibles:\n' +
                              '- /start : Mensaje de bienvenida. Muestra la lista de comandos disponibles\n' +
                              '- /foto: Toma una foto con la PiCamera y se muestra por chat\n' + 
                              '- /fotos_intervalo arg: Toma una foto con la PiCamera periódicamente cada "arg" segundos y se muestra por chat\n' +
                              '- /stop: Detiene la toma periódica de fotos\n')

# Función para la captura de 1 foto
def foto(update: Update, context: CallbackContext):
    # Nombre de guardado de la imagen
    fImagen = "imagen.jpg"
    # Toma de foto
    camera.capture(fImagen)
    # Envío de foto por el chat del bot de Telegram
    context.bot.send_photo(chat_id=update.message.chat_id, photo=open(fImagen, 'rb'))

# Función para la toma continua de fotos cada "arg" segundos
def fotos_intervalo(update: Update, context: CallbackContext):
    # Variables globales a modificar
    global fotos_intervalo_flag, msg_flag, timer
    # Si el argumento indicado por chat ("arg") no es un número o se pasa más de 1 argumento
    # se pide que se introduzca un intervalo válido de tiempo
    if len(context.args) != 1 or not context.args[0].isdigit():
        update.message.reply_text('Por favor, proporciona un intervalo de tiempo válido en segundos.')
        return
    # Se guarda el intervalo pasado como argumento
    intervalo = int(context.args[0])
    # La primera vez que se llama al comando se imprime un mensaje informativo
    if msg_flag:
        update.message.reply_text(f"Tomando fotos cada {intervalo} segundos. Para detener, envía /stop.")
    # Desactivamos la flag para no enviar más el mensaje
    msg_flag = False
    # La primera vez que se llama al comando se inicia la captura de fotos continua
    if fotos_intervalo_flag:
        # Nombre imagen
        fImagen = "imagen.jpg"
        # Captura de foto
        camera.capture(fImagen)
        # Envío por chat de bot de Telegram
        context.bot.send_photo(chat_id=update.message.chat_id, photo=open(fImagen, 'rb'))
        # Se define un timer que ejecuta la función periódicamente cada "intervalo" segundos
        timer = Timer(intervalo, fotos_intervalo, args=(update, context))
        # Se inicia el timer
        timer.start()

# Función para la detención del modo de captura continua de fotos
def stop(update: Update, context: CallbackContext):
    # Variables globales a modificar
    global fotos_intervalo_flag, msg_flag, timer
    # Se desactiva el flag de toma de fotos continua
    fotos_intervalo_flag = False
    # Se imprime un mensaje informativo por chat
    update.message.reply_text('Se ha detenido la captura periódica de fotos.')
    # Se cancela el timer
    timer.cancel()
    # Se vuelven a activar las flags para la siguiente llamada a la función "fotos_intervalo"
    fotos_intervalo_flag = True
    msg_flag = True

# Main
def main():
    # Se crea un objeto Updater que maneja todos los mensajes del bot de Telegram
    updater = Updater(TOKEN)
    # Se coge el objeto "dispatcher" del objeto creado previamente, que se encargará
    # de manejar y enviar los mensajes entrantes a los manejadores correspondientes
    dp = updater.dispatcher
    # El comando /start ejecuta la función "start"
    dp.add_handler(CommandHandler("start", start))
    # El comando /foto ejecuta la función "foto"
    dp.add_handler(CommandHandler("foto", foto))
    # El comando /fotos_intervalo "arg" ejecuta la función "fotos_intervalo"
    dp.add_handler(CommandHandler("fotos_intervalo", fotos_intervalo))
    # El comando /stop ejecuta la función "stop"
    dp.add_handler(CommandHandler("stop", stop))
    # Comprobación periódica de nuevos mensajes mediante "polling"
    updater.start_polling()
    # Corre el programa mientras no se pulse Ctrl+C o se detiene explícitamente el programa
    updater.idle()

# Si el script se está ejecutando como programa principal se llama a la función "main"
if __name__ == '__main__':
    main()
