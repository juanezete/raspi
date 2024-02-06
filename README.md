
# RaspiBot & RaspiCamBot 🤖🍓
Este proyecto engloba dos bots de Telegram: **RaspiBot** y **RaspiCamBot**. Ambos bots están diseñados para interactuar con imágenes, pero tienen funcionalidades distintas.

## RaspiBot
**Descripción:**

RaspiBot utiliza el modelo YOLO para analizar imágenes que le son enviadas a través de Telegram. Devuelve una imagen segmentada y una respeusta de texto con los objetos detectados.

**Uso:**

1. Inicia una conversación con RaspiBot en Telegram.
2. Utiliza `/start` para comenzar la interacción.
3. Envía una imagen y obtén una imagen segmentada con objetos detectados.
4. Ajusta la confianza del modelo con `/conf` <valor>.

**Estructura del Proyecto:**

`raspibot/` 

    `raspibot.py` Código principal de RaspiBot.

    `raspibot/codigo_antiguo` Códigos antiguos y subpartes del desarrollo.


## RaspiCamBot
**Descripción:**

RaspiCamBot está diseñado para capturar imágenes periódicas utilizando la cámara de Raspberry Pi. Las imágenes se pueden solicitar mediante comandos desde Telegram.

**Uso:**

1. Inicia una conversación con RaspiCamBot en Telegram.
2. Utiliza comandos como `/takepic` para solicitar imágenes de la cámara.


**Estructura del Proyecto:**

`raspicambot/` 


## Authors

- [@guillermonb](https://github.com/guillermonb)
- [@juanezete](https://github.com/juanezete)


