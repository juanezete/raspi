# RaspiBot & RaspiCamBot 🤖🍓📷
Este proyecto engloba dos bots de Telegram: **RaspiBot** y **RaspiCamBot**. Ambos bots están diseñados para interactuar con imágenes, pero tienen funcionalidades distintas.

## RaspiBot🤖👀 

**Descripción:** 👋

RaspiBot utiliza el modelo YOLO para analizar imágenes que le son enviadas a través de Telegram. Devuelve una imagen segmentada y una respuesta de texto con los objetos detectados.

**Uso:** 👨‍💻

1. Inicia una conversación con [RaspiBot](https://t.me/proyectosda_bot) en Telegram.
2. Utiliza `/start` para comenzar la interacción.
3. Envía una imagen y obtén una imagen segmentada con objetos detectados.
4. Ajusta la confianza del modelo con `/conf` <valor>.

**Estructura del Proyecto:** 🗃️

`raspibot/` 

    `raspibot.py` Código principal de RaspiBot.

    `raspibot/codigo_antiguo` Códigos antiguos y subpartes del desarrollo.


## RaspiCamBot
**Descripción:** 👋

RaspiCamBot está diseñado para capturar imágenes, tanto individuales como de forma periódica utilizando la cámara de Raspberry Pi.

**Uso:** 👨‍💻

1. Inicia una conversación con [RaspiCamBot](https://t.me/proyectosda2_bot) en Telegram.
2. Utiliza el comando `/start` para conocer la lista de comandos disponibles.
3. Utiliza el comando `/foto` para tomar una foto individual con la PiCamera.
4. Utiliza el comando `/fotos_intervalo` seguido de un argumento para tomar fotos de forma periódica cada <argumento> segundos. Por ejemplo, el comando `/fotos_intervalo 2` tomará fotos periódicamente cada 2 segundos.
5. Utiliza el comando `/stop` para detener la captura continua de fotos.


**Estructura del Proyecto:** 🗃️

`raspicambot/` 

    `raspicambot.py` Código principal de RaspiCamBot.


## Authors 👷‍♂️

- [@guinieben](https://github.com/guinieben)
- [@juanezete](https://github.com/juanezete)


