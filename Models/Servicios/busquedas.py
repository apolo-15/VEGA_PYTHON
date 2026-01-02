from urllib.parse import quote_plus
import webbrowser
import wikipedia

BUSCADORES = ("youtube", "spotify", "wikipedia")

def limpiar_busqueda(texto, proveedor):
    texto = texto.lower()
    texto = texto.replace("vega", "")
    texto = texto.replace("busca", "")
    texto = texto.replace(f"en {proveedor}", "")
    return texto.strip()

def buscar(proveedor, texto):
    consulta = quote_plus(texto)

    if proveedor == "youtube":
        url = f"https://www.youtube.com/results?search_query={consulta}"
        mensaje = f"Buscando '{texto}' en YouTube"
        webbrowser.open(url)
        return mensaje

    if proveedor == "spotify":
        url = f"https://open.spotify.com/search/{consulta}"
        mensaje = f"Buscando '{texto}' en Spotify"
        webbrowser.open(url)
        return mensaje

    if proveedor == "wikipedia":
        wikipedia.set_lang("es")
        resumen = wikipedia.summary(texto, 1)
        return resumen
    return None