from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Coloca aqui tu token proporcionado por BotFather en Telegram
TOKEN = '6472811121:AAEnTwQtPkaq4EYC9wOXzKCRU4dwtthATb0'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hola! Soy tu bot. Enviame una imagen y procesare algo con ella.')

def process_image(update: Update, context: CallbackContext) -> None:
    # Verifica si el mensaje contiene una foto
    if update.message.photo:
        # Obtiene la informacion de la foto
        photo = update.message.photo[-1]
        file_id = photo.file_id

        # Descarga la imagen
        file = context.bot.get_file(file_id)
        file.download('imagen_recibida.jpg')

        # Aqui puedes realizar cualquier procesamiento que desees con la imagen
        # Por ejemplo, puedes usar bibliotecas como Pillow para manipular la imagen

        # Respuesta al usuario
        update.message.reply_text('Imagen recibida y procesada con exito!')

    else:
        update.message.reply_text('Por favor, envia una imagen.')

def main() -> None:
    updater = Updater(TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.photo, process_image))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
