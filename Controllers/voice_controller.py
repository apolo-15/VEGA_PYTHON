from Audio.voice_listener import VoiceListenerThread

def reconocer_voz(ui, audio, on_text):
    ui.set_listening(True)

    voice_thread = VoiceListenerThread(audio)

    def procesar_texto(texto):
        texto = texto.replace("venga", "vega")
        texto = texto.replace("vega", "Vega")
        ui.mostrar_texto(f"Pablo: {texto}\n")
        on_text(texto)

    voice_thread.texto_reconocido.connect(procesar_texto)
    voice_thread.finished_listening.connect(
        lambda: ui.set_listening(False)
    )

    voice_thread.start()

    return voice_thread
