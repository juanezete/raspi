import cv2
from PIL import Image

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 224)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 224)
cap.set(cv2.CAP_PROP_FPS, 36)

ret, frame = cap.read()

if ret:
    image=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    
    pil_image=Image.fromarray(image)
    
    pil_image.show()

cap.release()