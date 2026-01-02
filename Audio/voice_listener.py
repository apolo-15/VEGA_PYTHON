from PySide6.QtCore import QThread, Signal

class VoiceListenerThread(QThread):
    texto_reconocido = Signal(str)
    finished_listening = Signal()

    def __init__(self, audio_service):
        super().__init__()
        self.audio = audio_service

    def run(self):
        texto = self.audio.escuchar()
        if texto:
            self.texto_reconocido.emit(texto)
        self.finished_listening.emit()
