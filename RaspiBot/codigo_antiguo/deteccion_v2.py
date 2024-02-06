from ultralytics import YOLO
from PIL import Image
import json

#Ruta del archivo de la imagen original
foto_path = '/home/juan/Desktop/codigo/fotos/imagen.jpg'

#Ruta del archivo json que asocia emojis
emojis_path = "/home/juan/Desktop/codigo/emojis.json"

# Se carga modelo de Yolo y se realiza la deteccion
model = YOLO("yolov8n.pt")
results = model(foto_path,conf = 0.4)

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

# Se imprime como depuracion
print(result_text)

# Bucle para mostrar los objetos sobre la imagen procesada
for r in results:
    im_array = r.plot()  # plot a BGR numpy array of predictions
    im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
    im.show()  # show image
    im.save('results.jpg')  # save image

