import webbrowser
import time
import pyautogui as pag


CONTACTS = {
    "cris": "+34653506407",
    "pablo": "+34689288924",
    "ecija": "+34644173072",
    "papa": "+34661989098",
    "mama": "+34670847006",
    "marta": "+34617663163",
}


def send_whatsapp(phone_number, message):
    if not phone_number or not message:
        return False

    url = f"https://web.whatsapp.com/send?phone={phone_number}&text={message}"
    webbrowser.open(url)

    time.sleep(10)
    pag.press("enter")

    return True
