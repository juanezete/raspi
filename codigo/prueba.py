from ultralytics import YOLO
from PIL import Image, ImageDraw
import os

foto_path = '/home/juan/Desktop/codigo/fotos/imagen.jpg'

# Load YOLO model
model = YOLO("yolov8n.pt")
results = model(foto_path)

for r in results:
    im_array = r.plot()  # plot a BGR numpy array of predictions
    im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
    im.show()  # show image
    im.save('results.jpg')  # save image