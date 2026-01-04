# LIBRARY IMPORTS
from datetime import datetime
from pathlib import Path
import sys

from PySide6.QtWidgets import QApplication


# PROJECT IMPORTS
from models.llm_model import VegaLLM
from views.main_window import VegaUI
from audio.audio_service import AudioService
from models.services.weather_service import CITIES
from controllers.chat_controller import handle_chat
from controllers.voice_controller import recognize_voice
from models.services.contacts_service import get_contacts


# ASSET PATHS
BASE_DIR = Path(__file__).resolve().parent
ASSETS_IMAGES = BASE_DIR / "assets_images"
ASSETS_TEXT = BASE_DIR / "assets_text"


# GLOBAL STATE
voice_thread = None


def main():
    llm = VegaLLM()
    audio_service = AudioService()

    current_date = datetime.now().strftime("%d-%m-%Y")

    context_holder = {"context": None}

    def handle_text_input(text: str):
        handle_chat(
            text,
            ui,
            audio_service,
            llm,
            get_contacts(ASSETS_TEXT),
            CITIES,
            ASSETS_TEXT,
            current_date,
            context_holder,
        )


    def handle_voice_input():
        global voice_thread
        voice_thread = recognize_voice(ui, audio_service, handle_text_input)

    app = QApplication(sys.argv)

    ui = VegaUI(
            ASSETS_IMAGES,
            ASSETS_TEXT,
            on_text=handle_text_input,
            on_voice=handle_voice_input,
        )


    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
