import pywhatkit


def play_youtube(query):
    if not query:
        return None

    pywhatkit.playonyt(query)
    return f"Reproduciendo {query}"
