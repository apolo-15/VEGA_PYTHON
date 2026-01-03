import webbrowser
import time
import pyautogui as pag

def enviar_whatsapp(numero, mensaje):
    if not numero or not mensaje:
        return False

    url = f"https://web.whatsapp.com/send?phone={numero}&text={mensaje}"
    webbrowser.open(url)

    time.sleep(10)
    pag.press("enter")

    return True
