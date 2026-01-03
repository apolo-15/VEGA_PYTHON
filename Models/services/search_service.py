from urllib.parse import quote_plus
import webbrowser
import wikipedia


SEARCH_PROVIDERS = ("youtube", "spotify", "wikipedia")


def clean_search_query(text, provider):
    text = text.lower()
    text = text.replace("vega", "")
    text = text.replace("search", "")
    text = text.replace(f"on {provider}", "")
    return text.strip()


def search(provider, text):
    query = quote_plus(text)

    if provider == "youtube":
        url = f"https://www.youtube.com/results?search_query={query}"
        message = f"Searching '{text}' on YouTube"
        webbrowser.open(url)
        return message

    if provider == "spotify":
        url = f"https://open.spotify.com/search/{query}"
        message = f"Searching '{text}' on Spotify"
        webbrowser.open(url)
        return message

    if provider == "wikipedia":
        wikipedia.set_lang("en")
        summary = wikipedia.summary(text, 1)
        return summary

    return None
