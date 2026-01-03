from unidecode import unidecode
from Models import memoria
from Models.Servicios.busquedas import BUSCADORES, limpiar_busqueda, buscar
from Models.Servicios.reproduccion import reproducir_youtube
from Models.Servicios.tiempo import obtener_tiempo
from Models.Servicios.mensajeria import enviar_whatsapp


def chat(
    question,
    ui,
    audio,
    llm,
    contactos,
    ciudades,
    assets_text,
    fecha,
    context_holder,
):
    q = question.lower()
    context = context_holder["context"]

    # Leer memoria
    instrucciones = memoria.leer_instrucciones(assets_text)
    instrucciones_resumen = memoria.leer_instrucciones_resumen(assets_text)
    memoria_texto = memoria.leer_memoria(assets_text)

    # Buscar
    if "busca" in q:
        for proveedor in BUSCADORES:
            if proveedor in q:
                texto = limpiar_busqueda(question, proveedor)
                resultado = buscar(proveedor, texto)
                if resultado:
                    ui.mostrar_texto(f"Vega: {resultado}\n")
                    audio.hablar(resultado)
                return

    # Reproducir
    if "reproduce" in q:
        texto = q.replace("vega", "").replace("reproduce", "").strip()
        resultado = reproducir_youtube(texto)

        if resultado:
            ui.mostrar_texto(f"Vega: {resultado}\n")
            audio.hablar(resultado)
        return

    # Tiempo
    if "tiempo hace" in q:
        for ciudad in ciudades:
            if ciudad in q:
                datos = obtener_tiempo(ciudad)

                if datos:
                    ui.mostrar_texto(f"Vega: El tiempo en {ciudad} es este:\n")
                    audio.hablar(f"El tiempo en {ciudad} es este")
                    for linea in datos:
                        ui.mostrar_texto(f"{linea}\n")
                else:
                    ui.mostrar_texto(f"Vega: No he podido obtener el tiempo de {ciudad}\n")
                    audio.hablar(f"No he podido obtener el tiempo de {ciudad}")
                return

    # Mensajería
    if "envia" in q:
        for contacto in contactos:
            if contacto in q:
                mensaje = None
                claves = ["que ", "diciendo ", "mensaje "]

                for clave in claves:
                    if clave in q:
                        mensaje = q.split(clave, 1)[1].strip()
                        break

                if not mensaje:
                    audio.hablar(f"¿Qué mensaje quieres enviar a {contacto}?")
                    ui.mostrar_texto(
                        f"\nVega: ¿Qué mensaje quieres enviar a {contacto}?\n"
                    )
                    mensaje = audio.escuchar()

                    if not mensaje:
                        audio.hablar("No te he entendido")
                        ui.mostrar_texto("Vega: No te he entendido\n")
                        return

                enviado = enviar_whatsapp(contactos[contacto], mensaje)

                if enviado:
                    audio.hablar(f"Mensaje enviado a {contacto}")
                    ui.mostrar_texto(f"Vega: Mensaje enviado a {contacto}\n")
                else:
                    audio.hablar("No he podido enviar el mensaje")
                    ui.mostrar_texto("Vega: No he podido enviar el mensaje\n")
                return

    # Cortar
    if "corta" in q:
        resumen = llm.resumir(instrucciones_resumen, context)
        resumen = unidecode(resumen)
        memoria.guardar_resumen(assets_text, resumen)
        ui.mostrar_texto("\nVega: Resumen guardado en memoria.\n")
        audio.hablar("Resumen guardado en memoria.")
        return

    # Conversación normal
    if context is None:
        context = ""

    result = llm.responder(
        fecha,
        instrucciones,
        memoria_texto,
        context,
        question,
    )
    result = unidecode(result)

    ui.mostrar_texto(f"\nVega: {result}\n")
    audio.hablar(result)

    context += f"Pablo: {question}\nVega: {result}\n"
    context_holder["context"] = context
