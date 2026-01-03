import webbrowser
import time
import pyautogui as pag

CONTACTOS = {
    "cris": "+34653506407",
    "pablo": "+34689288924",
    "ecija": "+34644173072",
    "papa": "+34661989098",
    "mama": "+34670847006",
    "marta": "+34617663163",
}


def enviar_whatsapp(numero, mensaje):
    if not numero or not mensaje:
        return False

    url = f"https://web.whatsapp.com/send?phone={numero}&text={mensaje}"
    webbrowser.open(url)

    time.sleep(10)
    pag.press("enter")

    return True
