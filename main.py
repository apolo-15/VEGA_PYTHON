# LIBS IMPORTS
from datetime import datetime
from pathlib import Path
from PySide6.QtWidgets import QApplication
import sys


# FILES IMPORTS
from Models.llm import VegaLLM
from Views.interfaz_qt import VegaUI
from Audio.audio_service import AudioService
from Models.Servicios.tiempo import CIUDADES
from Models.Servicios.mensajeria import CONTACTOS
from Controllers.chat_controller import chat
from Controllers.voice_controller import reconocer_voz


#ASSET PATHS
BASE_DIR = Path(__file__).resolve().parent
ASSETS_IMAGES = BASE_DIR / "Assets_Images"
ASSETS_TEXT = BASE_DIR / "Assets_Text"


#GLOBAL VARIABLES
voice_thread = None

def programa():

    #Definimos el modelo LLM
    llm = VegaLLM()

    #Definimos el servicio de audio
    audio = AudioService()

    #Definir la fecha actual
    dt = datetime.now()
    fecha=dt.strftime("%d-%m-%Y")


    context_holder = {"context": None}


    def on_text(texto):
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

    def on_voice():
        global voice_thread
        voice_thread = reconocer_voz(ui, audio, on_text)


    app = QApplication(sys.argv)

    ui = VegaUI(
            ASSETS_IMAGES,
            on_text=on_text,
            on_voice=on_voice,
        )


    ui.show()
    sys.exit(app.exec())

    
if __name__ == "__main__":
    programa()