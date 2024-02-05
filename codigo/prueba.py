from ultralytics import YOLO
from PIL import Image, ImageDraw
import os
foto_path = '/home/pi/Desktop/codigo/fotos/1.jpg'
# Ruta donde guardar la foto procesada
foto_procesada_path = '/home/pi/Desktop/codigo/fotos/1_procesada.jpg'
# Load YOLO model
model = YOLO("yolov8n.pt")
results = model(foto_path)

print("Muestro resultados")
print(results)
print("Fin de muestra de resultados")

# Obtiene la imagen original
image_original = Image.open(foto_path)
# Crea un objeto ImageDraw para dibujar en la imagen original
draw = ImageDraw.Draw(image_original)

# Verificar la existencia de resultados y cajas no nulas en el objeto Results
if results and results.boxes is not None:
    # Iterar sobre las cajas en el objeto Results
    for box, conf, label in zip(results.boxes.xyxy, results.boxes.conf, results.names):
        # Verificar la confianza
        if conf is not None and conf > 0.5:
            box = box.tolist()  # Convertir de tensor a lista
            draw.rectangle(box, outline="red", width=2)
            draw.text((box[0], box[1]), f"{label} {conf:.2f}", fill="red")

    # Guardar la imagen procesada
    image_original.save(foto_procesada_path)

    # Mostrar la imagen procesada
    image_original.show()
else:
    print("No se detectaron objetos en la imagen.")