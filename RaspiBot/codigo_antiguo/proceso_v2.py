from telegram import Update
from ultralytics import YOLO
from PIL import Image
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import json

# Token especifico del raspi bot
TOKEN = '6472811121:AAEnTwQtPkaq4EYC9wOXzKCRU4dwtthATb0'

# Respuesta ante comando start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hola! Soy RaspiBot \U0001F916 . Enviame una imagen y detectare objetos.')

#Respuesta ante el envio de una imagen
def process_image(update: Update, context: CallbackContext) -> None:
    # Verifica si el mensaje contiene una foto
    if update.message.photo:
        # Obtiene la informacion de la foto
        photo = update.message.photo[-1]
        file_id = photo.file_id

        # Descarga la imagen
        file = context.bot.get_file(file_id)
        file.download('imagen_recibida.jpg')
        
        #Contesta que la imagen ha sido recibida
        update.message.reply_text('Imagen recibida, procesando ... \u23F3')
        print('Imagen recibida, procesando ...')


        #Ruta del archivo de la imagen original
        foto_path = '/home/juan/Desktop/codigo/imagen_recibida.jpg'
        
        #Ruta del archivo json que asocia emojis
        emojis_path = "/home/juan/Desktop/codigo/emojis.json"
        
        # Se carga modelo de Yolo y se realiza la deteccion
        model = YOLO("yolov8n.pt")
        results = model(foto_path,conf = 0.6)
        
        # Se extraen las clases y el numero de ellas
        classes = results[0].boxes.cls.tolist()
        names = results[0].names

        # Se crea un diccionario para contar la cantidad de cada clase
        class_counts = {}

        # Se cargan los emojis del json
        with open(emojis_path, 'r') as f:
            emojis = json.load(f)

        # Se cuentan la cantidad de cada clase
        for class_index in classes:
            class_name = names[int(class_index)]
            class_counts[class_name] = class_counts.get(class_name, 0) + 1

        # Se crea una cadena de texto con la informacion
        result_text = "Objetos detectados:\n"
        # Se verfica si no se detectaron objetos
        if not class_counts:
            result_text += "No se ha detectado nada \u274C \n"
        else:
            for class_name, count in class_counts.items():
                result_text += f"{count} {class_name}(s) {emojis[class_name]}\n"
        
        for r in results:
            im_array = r.plot()  # plot a BGR numpy array of predictions
            im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
            im.save('results.jpg')  # save image
        
        try:
            # Se envia la imagen con los objetos detectados de vuelta al usuario
            context.bot.send_photo(chat_id=update.message.chat_id, photo=open('/home/juan/Desktop/codigo/results.jpg', 'rb'))
        except Exception as e:
            print(f"Error al enviar la imagen diferente: {e}") 

        # Se imprime como depuracion los resultados de la segmentacion
        print(result_text)
        # Respuesta al usuario
        update.message.reply_text(result_text)

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


