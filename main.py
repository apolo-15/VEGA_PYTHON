#OLLAMA IMPORTS
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

#OTHER IMPORTS
from tkinter.scrolledtext import ScrolledText
from tkinter import *
from PIL import Image, ImageTk
from unidecode import unidecode
import tkinter as tk
import re
import pyttsx3
import os
from datetime import datetime
import webbrowser
import time
import pywhatkit
import speech_recognition as sr
import wikipedia
import webbrowser
import pyautogui as pag
import requests
from pathlib import Path

#ASSET PATHS
BASE_DIR = Path(__file__).resolve().parent
ASSETS_IMAGES = BASE_DIR / "Assets_Images"
ASSETS_TEXT = BASE_DIR / "Assets_Text"





context = None
def programa():
    #Interfaz Fondo
    pag_principal = Tk()
    pag_principal.title("VEGA")
    pag_principal.geometry("1920x1080")
    pag_principal.configure(bg="#E2E2E2")

    #Interfaz Comandos de VEGA
    comandos = """
            Comandos:

            - Reproduce... (canción)
            - Busca... (Youtube, Spotify, Wikipedia)
            - Abre...
                - Discord
                - Spotify
                - Google
                - Steam
            - Envia... a...
            - Corta 
        """
    canvas_comandos = Canvas(bg="#c31432", height = 190, width = 280)
    def mostrar_comandos():
        if canvas_comandos.winfo_viewable():
            canvas_comandos.place_forget()
        else:
            canvas_comandos.place(x = 0, y = 50)
            canvas_comandos.create_text(120, 95, text = comandos, fill = "white", font = ("Arial", 10, "bold"))


    #Interfaz Cabina de escritura
    texto_info = Text(pag_principal, bg = "#c31432", fg = "white", font = ("Arial", 15, "bold"))
    texto_info.place(x = 610, y = 500, height = 400, width = 700)


    #Interfaz Título
    titulo = Label(pag_principal, text = "V E G A", bg = "#E2E2E2", fg = "#c31432", 
                font = ("Impact", 70))
    titulo.pack(pady=30)


    #VEGA Logo
    vega_logo = ImageTk.PhotoImage(Image.open(ASSETS_IMAGES / "vega_logo.png"))
    foto_pagina = Label(pag_principal, image=vega_logo, borderwidth=0, highlightthickness=0)
    foto_pagina.pack(pady=10)


    #LATERAL IZQUIERDO
    vega_lati = ImageTk.PhotoImage(Image.open(ASSETS_IMAGES / "lateral_izq.png"))
    foto_lati = Label(pag_principal, image=vega_lati)
    foto_lati.place(x = 1520, y = 0, height = 1080, width = 400)


    #LATERAL DERECHO
    vega_latd = ImageTk.PhotoImage(Image.open(ASSETS_IMAGES / "lateral_der.png"))
    foto_latd = Label(pag_principal, image=vega_latd)
    foto_latd.place(x = 0, y = 240, height = 840, width = 284)


    #Definir la fecha actual
    dt = datetime.now()
    fecha=dt.strftime("%d-%m-%Y")


    engine = pyttsx3.init()
    #Función para que Vega hable
    def texto_a_voz(texto):
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 1.0)
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)
        engine.say(texto)
        engine.runAndWait()


    #Plantilla de Vega
    plantilla = """
    Fecha de hoy: {fecha}

    Instrucciones obligatorias:
    {instrucciones}

    Memoria:
    {memoria}

    Topic de conversación:
    {context}

    Responde lo siguiente:
    {question}

    Respuesta:

    """


    #Plantilla del resumen
    mapa_mental = """
    Sigue estas instrucciones:
    {instrucciones_resumen}
    Resume esto siguiendo las instrucciones:
    {context}
    """


    #Informacion sobre el modelo
    model = OllamaLLM(model = "llama3.2")


    #Definimos el generador de texto
    prompt = ChatPromptTemplate.from_template(plantilla)
    chain = prompt | model


    #Definimos el generador del resumen
    MP = ChatPromptTemplate.from_template(mapa_mental)
    cadena = MP | model


    #Diccionario de aplicaciones
    aplicaciones = {
        "spotify" : r"C:\Users\pablo\AppData\Roaming\Spotify\Spotify.exe",
        "discord" : r"C:\Users\pablo\AppData\Local\Discord\Update.exe",
        "steam" : r"C:\Program Files (x86)\Steam\Steam.exe",
        "google" : r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    }


    #Contactos de whatssap
    contactos = {
        "cris" : "+34653506407",
        "blanca" : "+34658616957",
        "pablo" : "+34689288924",
        "ecija" : "+34644173072",
        "papa" : "+34661989098",
        "mama" : "+34670847006",
        "negrito" : "+34605812807"
    }


    #Ciudades para el tiempo
    ciudades = ["sevilla", "malaga", "madrid"]


    #Definimos las busquedas
    busquedas = ("youtube","spotify","wikipedia")



    #Funcion para escribir mensajes en la interfaz
    def escribir_interfaz(texto):
        print(texto)
        texto_info.insert(INSERT, texto)
        texto_info.update_idletasks()


    #Limpiar texto
    def limpiar_escribir(texto):
            # Limpia las secuencias ANSI antes de escribir
            cleaned_text = re.sub(r'\x1b\[[0-9;]*m', '', texto)
            escribir_interfaz(cleaned_text)


    #Borrar interfaz
    def borrar_interfaz():
        texto_info.delete("1.0",END)
        escribir_interfaz("---------------------------------------------------------------------------------------------------")


    #Copiar interfaz
    def copiar_interfaz():
        texto_copiar = texto_info.get("1.0",END)
        pag_principal.clipboard_clear()
        pag_principal.clipboard_append(texto_copiar)
        pag_principal.update
        escribir_interfaz(f"\nConversación copiada en el portapapeles\n")


    #Leer lo escrito sobre la interfaz
    def leer_interfaz():
        leer = texto_info.get("2.0",END)
        chat(leer)

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
                limpiar_escribir(f"{line}\n")
        else:
            print(f"Error al obtener la página: {response.status_code}")
        

    #Definimos el programa con el que interactuamos con VEGA
    
    def chat(question):
        global context
        # Leemos los distintos archivos
        with open(ASSETS_TEXT / 'instrucciones.txt', 'r') as archivo:
            instrucciones = archivo.read()
        with open(ASSETS_TEXT / 'instrucciones_resumen.txt', 'r') as archi:
            instrucciones_resumen = archi.read()
        with open(ASSETS_TEXT / 'memoria.txt', 'r') as arch:
            memoria = arch.read()

        #Definimos el contexto de la conversación vacío
        #Funcion de busqueda en Youtube
        def youtube(busqueda):
            query = busqueda.replace(" ","+")
            url = f"https://www.youtube.com/results?search_query={query}"
            webbrowser.open(url)
            escribir_interfaz(f"Vega: Buscando '{busqueda}' en Youtube.\n")
            texto_a_voz(f"Buscando '{busqueda}' en YouTube.")

        #Funcion de busqueda en Spotify
        def spotify(busqueda):
            query = busqueda.replace(" ","+")
            url = f"https://open.spotify.com/search/{query}?flow_ctx=c78838a4-c2a2-48f1-ad9c-77a481bea7fe%3A1737485819#login"
            webbrowser.open(url)
            escribir_interfaz(f"Vega: Buscando '{busqueda}' en Spotify.\n")
            texto_a_voz(f"Buscando '{busqueda}' en Spotify.")

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
                        escribir_interfaz(f"Vega: {wiki}")
                        texto_a_voz(f"Vega: {wiki}")
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
            escribir_interfaz(f"Vega: Reproduciendo {cancion}\n")
            texto_a_voz(f"Reproduciendo {cancion}")
            pywhatkit.playonyt(cancion)
            return

        #Abrir aplicaciones
        if "abre" in question:
            for app in aplicaciones:
                if app in question:
                    texto_a_voz(f"Abriendo {app}")
                    escribir_interfaz(f"Vega: Abriendo {app}\n")
                    os.startfile(aplicaciones[app])
            return                 


        

        #Tiempo
        if "tiempo hace" in question:
            for ciudad in ciudades:
                if ciudad in question:
                    escribir_interfaz(f"Vega: El en {ciudad} es este colega:\n")
                    texto_a_voz(f"El tiempo en {ciudad} es este colega:")
                    fetch_weather(ciudad)
            return


        #Enviar mensajes
        if "envia" in question:
            def mensaje_oir(contacto):
                recognizer = sr.Recognizer()
                # Usar el micrófono como fuente de entrada
                try:
                    with sr.Microphone() as source:
                        texto_a_voz(f"Le envio un mensaje a {contacto}. Que quieres que diga?")
                        escribir_interfaz(f"\nVega: Le envio un mensaje a {contacto}. Que quieres que diga?:\n")
                        escribir_interfaz(f"\nVega: Espera...\n")
                        recognizer.adjust_for_ambient_noise(source, duration=1)
                        escribir_interfaz(f"Vega: Di algo:\n")
                        # Escuchar el audio del micrófono
                        audio = recognizer.listen(source)
                        mensaje = recognizer.recognize_google(audio, language="es-ES")
                        mensaje = unidecode(mensaje)
                        mensaje = mensaje.lower()
                        escribir_interfaz(f"Pablo: {mensaje}\n")
                        texto_a_voz(f"enviando {mensaje} a {contacto}")
                        escribir_interfaz(f"Vega: Enviando '{mensaje}' a {contacto}\n")

                        enviar_mensaje(contacto, mensaje)

                except sr.UnknownValueError:
                    engine.say("Sácate la polla de la boca y repite")
                except sr.RequestError as e:
                    print(f"Error al comunicarse con Google Speech Recognition: {e}")
                
            for contacto in contactos:
                if contacto in question:
                    mensaje_oir(contacto)
            return       

        #Detener el programa
        if "corta" in question:
            #Resumen de las conversaciones
            resumen = cadena.invoke({"instrucciones_resumen": instrucciones_resumen,"context": context})
            resumen = unidecode(resumen)
            resumir(resumen)
            return

        if context == None:
            context = ""  
            #Motor de conversacion
            result = chain.invoke({"fecha": fecha,"instrucciones": instrucciones,"memoria": memoria,"context": context, "question": question})
            result = unidecode(result)
            print("Vega: ", result)
            escribir_interfaz(f"\nVega: {result}\n")
            texto_a_voz(result)
            context += f"Pablo: {question}\nVega: {result}\n"
            return

        else:
            #Motor de conversacion
            result = chain.invoke({"fecha": fecha,"instrucciones": instrucciones,"memoria": memoria,"context": context, "question": question})
            result = unidecode(result)
            print("Vega: ", result)
            escribir_interfaz(f"\nVega: {result}\n")
            texto_a_voz(result)
            context += f"Pablo: {question}\nVega: {result}\n"
            return


    #Voz a Texto:
    def reconocer_voz():
        recognizer = sr.Recognizer()
        # Usar el micrófono como fuente de entrada
        
        try:
            with sr.Microphone() as source:
                escribir_interfaz(f"\nVega: Espera...\n")
                recognizer.adjust_for_ambient_noise(source, duration=1)           
                escribir_interfaz(f"Vega: Di algo:\n")

                # Escuchar el audio del micrófono
                audio = recognizer.listen(source)
                texto = recognizer.recognize_google(audio, language="es-ES")
                texto = unidecode(texto)
                texto = texto.lower()
                texto = texto.replace("venga","vega")
                texto = texto.replace("vega", "Vega")
                escribir_interfaz(f"Pablo: {texto}\n")
                chat(texto)
        except sr.UnknownValueError:
            engine.say("Error")
        except sr.RequestError as e:
            print(f"Error al comunicarse con Google Speech Recognition: {e}")
        return texto




    # Archivo donde guardar las conversaciones
    filename = 'memoria.txt'

    #Guardar la memoria
    def resumir(resumen):
        # Verifica si el archivo existe, sino crea uno
        if not os.path.exists(filename):
            with open(filename, 'w') as f:
                f.write("Conversaciones iniciadas el: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n\n")
                f.write(resumen)
        # Guardar la conversación en el archivo (inactivo)
        with open(filename, 'a') as f:
            f.write("Conversaciones iniciadas el: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n\n")
            f.write(resumen)




    #Boton escucha
    vega_escucha = ImageTk.PhotoImage(Image.open(ASSETS_IMAGES / "escucha.png"))
    boton_escucha = Button(pag_principal, image=vega_escucha, command=reconocer_voz)
    boton_escucha.place(x=910, y=370, width=100, height=100)

    #Boton borrar
    papelera = ImageTk.PhotoImage(Image.open(ASSETS_IMAGES / "papelera.png"))
    boton_papelera = Button(pag_principal, image=papelera, command=borrar_interfaz)
    boton_papelera.place(x=820, y=420, width=50, height=50)

    #Boton copiar
    copiar = ImageTk.PhotoImage(Image.open(ASSETS_IMAGES / "copiar.png"))
    boton_copiar = Button(pag_principal, image=copiar, command=copiar_interfaz)
    boton_copiar.place(x=1050, y=420, width=50, height=50)

    #Boton copiar
    leer_int = ImageTk.PhotoImage(Image.open(ASSETS_IMAGES / "leer.png"))
    boton_leer = Button(pag_principal, image=leer_int, command=leer_interfaz)
    boton_leer.place(x=1150, y=420, width=50, height=50)

    #Boton comandos
    boton_comandos = Button(pag_principal, text="Mostrar comandos", fg="white", bg="#c31432", font=("Arial", 15, "bold"), command=mostrar_comandos)
    boton_comandos.place(x=0, y=0, width=284, height=50)



    ##EJECUCIÓN DEL PROGRAMA
    escribir_interfaz("---------------------------------------------------------------------------------------------------")
    pag_principal.mainloop()
    
if __name__ == "__main__":
    programa()