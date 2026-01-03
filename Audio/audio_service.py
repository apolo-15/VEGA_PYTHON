import pyttsx3
from unidecode import unidecode
import speech_recognition as sr


class AudioService:
    def __init__(self):
        self._engine = None
        self._tts_available = True

    def _init_tts(self):
        """
        Initializes the TTS engine lazily, only when needed.
        """
        if self._engine is not None:
            return

        try:
            engine = pyttsx3.init()
            engine.setProperty("rate", 180)
            engine.setProperty("volume", 1.0)

            voices = engine.getProperty("voices")
            if voices:
                engine.setProperty("voice", voices[0].id)

            self._engine = engine

        except Exception as error:
            # If TTS fails, VEGA must continue silently
            print(f"[AudioService] Error initializing TTS: {error}")
            self._tts_available = False
            self._engine = None

    def speak(self, text: str):
        """
        Converts text to speech.
        Fails silently if audio is not available.
        """
        if not self._tts_available or not text:
            return

        self._init_tts()

        if self._engine is None:
            return

        try:
            text = unidecode(text)
            self._engine.say(text)
            self._engine.runAndWait()
        except Exception as error:
            print(f"[AudioService] Error while speaking: {error}")
            self._tts_available = False

    def listen(self, timeout=None):
        """
        Listens through the microphone and returns recognized text in lowercase.
        Returns None if recognition fails or no speech is detected.
        """
        try:
            recognizer = sr.Recognizer()

            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = recognizer.listen(source, timeout=timeout)

            text = recognizer.recognize_google(audio, language="es-ES")
            text = unidecode(text).lower()
            return text

        except sr.UnknownValueError:
            return None

        except sr.RequestError as error:
            print(f"[AudioService] Speech Recognition request error: {error}")
            return None

        except Exception as error:
            print(f"[AudioService] Error while listening: {error}")
            return None
