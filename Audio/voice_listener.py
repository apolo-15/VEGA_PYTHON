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
