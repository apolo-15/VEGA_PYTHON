# LIBS IMPORTS
from datetime import datetime
from pathlib import Path
from PySide6.QtWidgets import QApplication
import sys


# FILES IMPORTS
from Models.llm import VegaLLM
from Views.interfaz_qt import VegaUI
from Audio.audio_service import AudioService
from Audio.voice_listener import VoiceListenerThread
from Models.Servicios.tiempo import CIUDADES
from Models.Servicios.mensajeria import CONTACTOS
from Controllers.chat_controller import chat


#ASSET PATHS
BASE_DIR = Path(__file__).resolve().parent
ASSETS_IMAGES = BASE_DIR / "Assets_Images"
ASSETS_TEXT = BASE_DIR / "Assets_Text"


# Lugar temporal
voice_thread = None
context = None

def programa():

    #Definimos el modelo LLM
    llm = VegaLLM()

    #Definimos el servicio de audio
    audio = AudioService()

    #Definir la fecha actual
    dt = datetime.now()
    fecha=dt.strftime("%d-%m-%Y")


    context_holder = {"context": None}


    #Voz a Texto:
    def reconocer_voz():
        global voice_thread

        ui.set_listening(True)

        voice_thread = VoiceListenerThread(audio)

        def procesar_texto(texto):
            texto = texto.replace("venga", "vega")
            texto = texto.replace("vega", "Vega")
            ui.mostrar_texto(f"Pablo: {texto}\n")
            chat(
                texto,
                ui,
                audio,
                llm,
                CONTACTOS,
                CIUDADES,
                ASSETS_TEXT,
                fecha,
                context_holder,
            )


        voice_thread.texto_reconocido.connect(procesar_texto)
        voice_thread.finished_listening.connect(lambda: ui.set_listening(False))

        voice_thread.start()




    app = QApplication(sys.argv)

    ui = VegaUI(
            ASSETS_IMAGES,
            on_text=lambda texto: chat(
                texto,
                ui,
                audio,
                llm,
                CONTACTOS,
                CIUDADES,
                ASSETS_TEXT,
                fecha,
                context_holder,
            ),
            on_voice=reconocer_voz,
        )


    ui.show()
    sys.exit(app.exec())

    
if __name__ == "__main__":
    programa()