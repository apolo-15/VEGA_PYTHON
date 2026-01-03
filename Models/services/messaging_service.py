import webbrowser
import time
import pyautogui as pag


def send_whatsapp(phone_number: str, message: str) -> bool:
    if not phone_number or not message:
        return False

    url = f"https://web.whatsapp.com/send?phone={phone_number}&text={message}"
    webbrowser.open(url)

    time.sleep(10)
    pag.press("enter")

    return True
