# PABLO BOTELLA JIMÉNEZ
# Vega AI Assistant Application

# Voice listener thread module for the Vega AI assistant application.
# Implements a QThread to handle voice recognition in the background,
# emitting signals when text is recognized or when listening is finished.
# Minimun logic is handled in this file; most functionality is delegated to controllers and models.

# LIBRARY IMPORTS
from PySide6.QtCore import QThread, Signal


class VoiceListenerThread(QThread):
    text_recognized = Signal(str)
    finished_listening = Signal()

    def __init__(self, audio_service):
        super().__init__()
        self.audio_service = audio_service

    def run(self):
        text = self.audio_service.listen()
        if text:
            self.text_recognized.emit(text)
        self.finished_listening.emit()
