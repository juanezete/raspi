#Importamos las librerias necesarias
from telegram import Update
from ultralytics import YOLO
from PIL import Image
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import json

# Token especifico del raspi bot
TOKEN = '6472811121:AAEnTwQtPkaq4EYC9wOXzKCRU4dwtthATb0'

# Se define la respuesta ante comando start de telegram
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hola! Soy RaspiBot \U0001F916 . Enviame una imagen y detectare objetos.'
        '\n\nTambien puedes ajustar la confianza del modelo \U0001F3AF entre 0 y 1 usando /conf.'
        '\nPor ejemplo, /conf 0.8 establecera la confianza en 0.8.'
        '\n\n\u26A0Recomendable\u26A0 usar una conf > 0.4 para resultados aceptables')

# Se define una funcion para manejar el comando /conf
def set_conf(update: Update, context: CallbackContext) -> None:
    args = context.args
    # Si no se proporciona algun valor despues del comando
    if not args:
        update.message.reply_text('Por favor, proporciona un valor entre 0 y 1 despues de /conf.')
        return
    
    try:
        new_conf = float(args[0])
        #Se comprueba que el valor de confianza esta entre 0 y 1
        if 0 <= new_conf <= 1:
            context.user_data['telegram_conf'] = new_conf
            update.message.reply_text(f'Se ha ajustado la confianza del modelo a {new_conf}.')
            #Se comprueba si esta por encima de 0.4 para dar buenas predicciones
            if new_conf < 0.4:
                 update.message.reply_text(f'¡Cuidado!\u26A0\nPuede haber malas predicciones {new_conf} < 0.4.')
        else:
            update.message.reply_text('El valor debe estar entre 0 y 1.')       
    except ValueError:
        update.message.reply_text('Por favor, proporciona un valor numerico valido.')

#Funcion de respuesta ante el envio de una imagen
def process_image(update: Update, context: CallbackContext) -> None:
    # Verifica si el mensaje contiene una foto
    if update.message.photo:
        # Obtiene la informacion de la foto
        photo = update.message.photo[-1]
        file_id = photo.file_id

        # Descarga la imagen
        file = context.bot.get_file(file_id)
        file.download('imagen_recibida.jpg')
        
        #Contesta con un mensaje que la imagen ha sido recibida + print de depuracion
        update.message.reply_text('Imagen recibida, procesando ... \u23F3')
        print('Imagen recibida, procesando ...')


        #Ruta del archivo de la imagen descargada desde telegram
        foto_path = '/home/juan/Desktop/codigo/imagen_recibida.jpg'
        
        #Ruta del archivo json que asocia emojis
        emojis_path = "/home/juan/Desktop/codigo/emojis.json"
        
        # Se asigna la confianza recibida por telegram
        telegram_conf = context.user_data.get('telegram_conf', 0.4)
        # Se carga el modelo de YOLO
        model = YOLO("yolov8n.pt")
        #Se procesa la imagen con la confianza deseada
        results = model(foto_path,conf = telegram_conf)
        
        # Se extraen las clases y el numero de estas
        classes = results[0].boxes.cls.tolist()
        names = results[0].names

        # Se crea un diccionario para contar la cantidad de cada clase
        class_counts = {}

        # Se cargan los emojis del archivo json
        with open(emojis_path, 'r') as f:
            emojis = json.load(f)

        # Se cuentan la cantidad de cada clase
        for class_index in classes:
            class_name = names[int(class_index)]
            class_counts[class_name] = class_counts.get(class_name, 0) + 1

        # Se crea una cadena de texto con toda la informacion
        result_text = "Objetos detectados:\n"
        # Se verfica si no se detectaron objetos
        if not class_counts:
            result_text += "No se ha detectado nada \u274C \n"
        else:
            # Se asigna numero total de clases y emoji caracteristico a cada una
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

        # Se imprime como depuracion los resultados de la segmentacion y se envia al usuario de vuelta
        print(result_text)
        update.message.reply_text(result_text)

    else:
        update.message.reply_text('Por favor, envia una imagen.')

def main() -> None:
    #Se crea una instancia con el token predeterminado del RaspiBot
    updater = Updater(TOKEN)

    #Obtiene el dispatcher necesario para la libreria
    dp = updater.dispatcher
    
    #Se agregan los manejadores para las 3 acciones posibles dentro del bot
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("conf", set_conf, pass_args=True))
    dp.add_handler(MessageHandler(Filters.photo, process_image))

    while True:
        try:
            #Inicia el proceso de escucha del bot
            updater.start_polling()
        except Exception as e:
            #Proceso que maneja posibles excepciones que se produzcan
            print(f"Error al iniciar el bot: {e}")
            time.sleep(5)  # Espera 5 segundos antes de intentar nuevamente

if __name__ == '__main__':
    main()



