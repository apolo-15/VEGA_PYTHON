# LIBS IMPORTS
from unidecode import unidecode
from datetime import datetime
from pathlib import Path
from PySide6.QtWidgets import QApplication
import sys


# FILES IMPORTS
from Models import memoria
from Models.llm import VegaLLM
from Views.interfaz_qt import VegaUI
from Audio.audio_service import AudioService
from Audio.voice_listener import VoiceListenerThread
from Models.Servicios.busquedas import BUSCADORES, limpiar_busqueda, buscar
from Models.Servicios.reproduccion import reproducir_youtube
from Models.Servicios.tiempo import obtener_tiempo
from Models.Servicios.mensajeria import enviar_whatsapp


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




    #Definimos el programa con el que interactuamos con VEGA   
    def chat(question):
        global context
        # Leemos los distintos archivos
        instrucciones = memoria.leer_instrucciones(ASSETS_TEXT)
        instrucciones_resumen = memoria.leer_instrucciones_resumen(ASSETS_TEXT)
        memoria_texto = memoria.leer_memoria(ASSETS_TEXT)


        #Buscar
        if "busca" in question.lower():
            for proveedor in BUSCADORES:
                if proveedor in question.lower():
                    texto = limpiar_busqueda(question, proveedor)
                    resultado = buscar(proveedor, texto)
                    if resultado:
                        ui.mostrar_texto(f"Vega: {resultado}\n")
                        audio.hablar(resultado)

                    return
            

        #Reproducir en YouTube
        if "reproduce" in question.lower():
            texto = question.lower()
            texto = texto.replace("vega", "")
            texto = texto.replace("reproduce", "")
            texto = texto.strip()

            resultado = reproducir_youtube(texto)

            if resultado:
                ui.mostrar_texto(f"Vega: {resultado}\n")
                audio.hablar(resultado)

            return



        #Tiempo
        if "tiempo hace" in question.lower():
            for ciudad in ciudades:
                if ciudad in question.lower():
                    datos = obtener_tiempo(ciudad)

                    if datos:
                        ui.mostrar_texto(f"Vega: El tiempo en {ciudad} es este:\n")
                        audio.hablar(f"El tiempo en {ciudad} es este")

                        for linea in datos:
                            ui.mostrar_texto(f"{linea}\n")

                    else:
                        ui.mostrar_texto(f"Vega: No he podido obtener el tiempo de {ciudad}\n")
                        audio.hablar(f"No he podido obtener el tiempo de {ciudad}")

                    return



        #Enviar mensajes
        if "envia" in question.lower():
            texto = question.lower()

            for contacto in contactos:
                if contacto in texto:

                    mensaje = None
                    claves = ["que ", "diciendo ", "mensaje "]

                    for clave in claves:
                        if clave in texto:
                            mensaje = texto.split(clave, 1)[1]
                            break

                    if mensaje:
                        mensaje = mensaje.strip()

                    if not mensaje:
                        audio.hablar(f"¿Qué mensaje quieres enviar a {contacto}?")
                        ui.mostrar_texto(f"\nVega: ¿Qué mensaje quieres enviar a {contacto}?\n")

                        mensaje = audio.escuchar()

                        if not mensaje:
                            audio.hablar("No te he entendido")
                            ui.mostrar_texto("Vega: No te he entendido\n")
                            return

                    enviado = enviar_whatsapp(contactos[contacto], mensaje)

                    if enviado:
                        audio.hablar(f"Mensaje enviado a {contacto}")
                        ui.mostrar_texto(f"Vega: Mensaje enviado a {contacto}\n")
                    else:
                        audio.hablar("No he podido enviar el mensaje")
                        ui.mostrar_texto("Vega: No he podido enviar el mensaje\n")

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