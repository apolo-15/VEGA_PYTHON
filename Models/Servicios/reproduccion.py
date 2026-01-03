import pywhatkit

def reproducir_youtube(texto):
    if not texto:
        return None

    pywhatkit.playonyt(texto)
    return f"Reproduciendo {texto}"
