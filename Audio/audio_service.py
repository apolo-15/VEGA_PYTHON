import pyttsx3
from unidecode import unidecode
import speech_recognition as sr


class AudioService:
    def __init__(self):
        self._engine = None
        self._tts_available = True

    def _init_tts(self):
        """
        Inicializa el motor TTS solo cuando se necesita.
        """
        if self._engine is not None:
            return

        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)
            engine.setProperty('volume', 1.0)

            voices = engine.getProperty('voices')
            if voices:
                engine.setProperty('voice', voices[0].id)

            self._engine = engine

        except Exception as e:
            # Si falla el audio, no debe caer VEGA
            print(f"[AudioService] Error inicializando TTS: {e}")
            self._tts_available = False
            self._engine = None

    def hablar(self, texto: str):
        """
        Convierte texto a voz. Si el audio no está disponible,
        falla en silencio.
        """
        if not self._tts_available:
            return

        if not texto:
            return

        self._init_tts()

        if self._engine is None:
            return

        try:
            texto = unidecode(texto)
            self._engine.say(texto)
            self._engine.runAndWait()
        except Exception as e:
            print(f"[AudioService] Error al hablar: {e}")
            self._tts_available = False

    def escuchar(self, timeout=None):
        """
        Escucha por micrófono y devuelve el texto reconocido en minúsculas.
        Devuelve None si falla o no se reconoce nada.
        """
        try:
            recognizer = sr.Recognizer()

            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = recognizer.listen(source, timeout=timeout)

            texto = recognizer.recognize_google(audio, language="es-ES")
            texto = unidecode(texto).lower()
            return texto

        except sr.UnknownValueError:
            # No se ha entendido la voz
            return None

        except sr.RequestError as e:
            print(f"[AudioService] Error con Speech Recognition: {e}")
            return None

        except Exception as e:
            print(f"[AudioService] Error al escuchar: {e}")
            return None

