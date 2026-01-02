# OTHER IMPORTS
from unidecode import unidecode
import re
from datetime import datetime
import webbrowser
import time
import pywhatkit
import wikipedia
import webbrowser
import pyautogui as pag
import requests
from pathlib import Path
from PySide6.QtWidgets import QApplication
import sys


# FILES IMPORTS
from Models import memoria
from Models.llm import VegaLLM
from Views.interfaz_qt import VegaUI
from Audio.audio_service import AudioService
from Audio.voice_listener import VoiceListenerThread


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


    #Contactos de whatssap
    contactos = {
        "cris" : "+34653506407",
        "pablo" : "+34689288924",
        "ecija" : "+34644173072",
        "papa" : "+34661989098",
        "mama" : "+34670847006",
        "marta" : "+34617663163"
    }


    #Ciudades para el tiempo
    ciudades = ["sevilla", "malaga", "madrid"]


    #Definimos las busquedas
    busquedas = ("youtube","spotify","wikipedia")



    #Funcion para enviar un mensaje por whatsapp
    def enviar_mensaje(contacto, mensaje):
        webbrowser.open(f"https://web.whatsapp.com/send?phone={contactos[contacto]}&text={mensaje}")
        time.sleep(10)
        pag.press("enter")




    #Tiempo
    def fetch_weather(ciudad):
        response = requests.get(f"https://es.wttr.in/{ciudad}")
        if response.status_code == 200:
            lines = response.text.splitlines()
            for i, line in enumerate(lines[2:7], start=1):
                ui.mostrar_texto(re.sub(r'\x1b\[[0-9;]*m', '', line))
        else:
            print(f"Error al obtener la página: {response.status_code}")
        

    #Definimos el programa con el que interactuamos con VEGA
    
    def chat(question):
        global context
        # Leemos los distintos archivos
        instrucciones = memoria.leer_instrucciones(ASSETS_TEXT)
        instrucciones_resumen = memoria.leer_instrucciones_resumen(ASSETS_TEXT)
        memoria_texto = memoria.leer_memoria(ASSETS_TEXT)

        #Definimos el contexto de la conversación vacío
        #Funcion de busqueda en Youtube
        def youtube(busqueda):
            query = busqueda.replace(" ","+")
            url = f"https://www.youtube.com/results?search_query={query}"
            webbrowser.open(url)
            ui.mostrar_texto(f"Vega: Buscando '{busqueda}' en Youtube.\n")
            audio.hablar(f"Buscando '{busqueda}' en YouTube.")

        #Funcion de busqueda en Spotify
        def spotify(busqueda):
            query = busqueda.replace(" ","+")
            url = f"https://open.spotify.com/search/{query}?flow_ctx=c78838a4-c2a2-48f1-ad9c-77a481bea7fe%3A1737485819#login"
            webbrowser.open(url)
            ui.mostrar_texto(f"Vega: Buscando '{busqueda}' en Spotify.\n")
            audio.hablar(f"Buscando '{busqueda}' en Spotify.")

        #Funcion de busqueda
        def buscar():
            for bus in busquedas:
                if bus in question:
                    busqueda = question.replace("Vega","")
                    busqueda = busqueda.replace("busca","")
                    busqueda = busqueda.replace(f"en {bus}","")
                    busqueda = busqueda.strip()
                    if bus == "youtube":
                        youtube(busqueda)
                    elif bus == "spotify":
                        spotify(busqueda)
                    elif bus == "wikipedia":
                        wikipedia.set_lang("es")
                        wiki = wikipedia.summary(busqueda, 1)
                        print("Vega: ", wiki)
                        ui.mostrar_texto(f"Vega: {wiki}")
                        audio.hablar(f"Vega: {wiki}")
                    time.sleep(1.5)
    

        #Buscar
        if "busca" in question:
            buscar()
            return
            

        #Reproducir videos en youtube
        if "reproduce" in question:
            cancion = question.replace("Vega","")
            cancion = question.replace("reproduce","")
            cancion = cancion.strip()
            print(f"Vega: Reproduciendo {cancion}")
            ui.mostrar_texto(f"Vega: Reproduciendo {cancion}\n")
            audio.hablar(f"Reproduciendo {cancion}")
            pywhatkit.playonyt(cancion)
            return


        #Tiempo
        if "tiempo hace" in question:
            for ciudad in ciudades:
                if ciudad in question:
                    ui.mostrar_texto(f"Vega: El en {ciudad} es este colega:\n")
                    audio.hablar(f"El tiempo en {ciudad} es este colega:")
                    fetch_weather(ciudad)
            return


        #Enviar mensajes
        if "envia" in question:
            def mensaje_oir(contacto):
                audio.hablar(f"Le envío un mensaje a {contacto}. ¿Qué quieres que diga?")
                ui.mostrar_texto(
                    f"\nVega: Le envío un mensaje a {contacto}. ¿Qué quieres que diga?\n"
                )
                ui.mostrar_texto("\nVega: Espera...\n")
                ui.mostrar_texto("Vega: Di algo:\n")

                mensaje = audio.escuchar()

                if mensaje is None:
                    audio.hablar("No te he entendido, intenta de nuevo")
                    ui.mostrar_texto("Vega: No te he entendido, intenta de nuevo\n")
                    return

                ui.mostrar_texto(f"Pablo: {mensaje}\n")
                audio.hablar(f"Enviando {mensaje} a {contacto}")
                ui.mostrar_texto(f"Vega: Enviando '{mensaje}' a {contacto}\n")

                enviar_mensaje(contacto, mensaje)

                
            for contacto in contactos:
                if contacto in question:
                    mensaje_oir(contacto)
            return       

        #Detener el programa
        if "corta" in question:
            #Resumen de las conversaciones
            resumen = llm.resumir(instrucciones_resumen,context,)
            resumen = unidecode(resumen)
            memoria.guardar_resumen(ASSETS_TEXT, resumen)
            ui.mostrar_texto("\nVega: Resumen guardado en memoria.\n")
            audio.hablar("Resumen guardado en memoria.")
            return

        if context == None:
            context = ""  
            #Motor de conversacion
            result = llm.responder(fecha,instrucciones,memoria_texto,context,question,)
            result = unidecode(result)
            print("Vega: ", result)
            ui.mostrar_texto(f"\nVega: {result}\n")
            audio.hablar(result)
            context += f"Pablo: {question}\nVega: {result}\n"
            return

        else:
            #Motor de conversacion
            result = llm.responder(fecha,instrucciones,memoria_texto,context,question,)
            result = unidecode(result)
            print("Vega: ", result)
            ui.mostrar_texto(f"\nVega: {result}\n")
            audio.hablar(result)
            context += f"Pablo: {question}\nVega: {result}\n"
            return


    #Voz a Texto:
    def reconocer_voz():
        global voice_thread

        ui.set_listening(True)

        voice_thread = VoiceListenerThread(audio)

        def procesar_texto(texto):
            texto = texto.replace("venga", "vega")
            texto = texto.replace("vega", "Vega")
            ui.mostrar_texto(f"Pablo: {texto}\n")
            chat(texto)

        voice_thread.texto_reconocido.connect(procesar_texto)
        voice_thread.finished_listening.connect(lambda: ui.set_listening(False))

        voice_thread.start()




    app = QApplication(sys.argv)

    ui = VegaUI(
    ASSETS_IMAGES,
    on_text=chat,
    on_voice=reconocer_voz,
    )

    ui.show()
    sys.exit(app.exec())

    
if __name__ == "__main__":
    programa()