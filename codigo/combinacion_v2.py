from telegram import Update
from ultralytics import YOLO
from PIL import Image, ImageDraw
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
        
        update.message.reply_text('Imagen recibida, procesando ...')

        # Aqui puedes realizar cualquier procesamiento que desees con la imagen
        foto_path = '/home/juan/Desktop/codigo/imagen_recibida.jpg'
        # Load YOLO model
        model = YOLO("yolov8n.pt")
        results = model(foto_path)

        for r in results:
            im_array = r.plot()  # plot a BGR numpy array of predictions
            im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
            im.save('results.jpg')  # save image
        
        try:
            # Reemplaza 'ruta_en_raspberry/imagen_diferente.jpg' con la ruta de tu imagen en la Raspberry Pi
            context.bot.send_photo(chat_id=update.message.chat_id, photo=open('/home/juan/Desktop/codigo/results.jpg', 'rb'))
        except Exception as e:
            print(f"Error al enviar la imagen diferente: {e}")
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

    while True:
        try:
            updater.start_polling()
        except Exception as e:
            print(f"Error al iniciar el bot: {e}")
            time.sleep(5)  # Espera 5 segundos antes de intentar nuevamente

if __name__ == '__main__':
    main()


