# PABLO BOTELLA JIMÉNEZ
# Vega AI Assistant Application

# Provides search functionality for the Vega AI assistant.
# Supports searching on YouTube, Spotify, and Wikipedia.
# Opens web browsers for YouTube and Spotify searches, and retrieves summaries from Wikipedia.

# LIBRARY IMPORTS
from urllib.parse import quote_plus
import webbrowser
import wikipedia

# ADD SEARCH PROVIDERS HERE
SEARCH_PROVIDERS = ("youtube", "spotify", "wikipedia")


def clean_search_query(text, provider):
    text = text.lower()
    text = text.replace("vega", "")
    text = text.replace("busca", "")
    text = text.replace(f"en {provider}", "")
    return text.strip()


def search(provider, text):
    query = quote_plus(text)

    if provider == "youtube":
        url = f"https://www.youtube.com/results?search_query={query}"
        message = f"Buscando '{text}' en YouTube"
        webbrowser.open(url)
        return message

    if provider == "spotify":
        url = f"https://open.spotify.com/search/{query}"
        message = f"Buscando '{text}' en Spotify"
        webbrowser.open(url)
        return message

    if provider == "wikipedia":
        wikipedia.set_lang("en")
        summary = wikipedia.summary(text, 1)
        return summary

    # Add more providers as needed

    return None
