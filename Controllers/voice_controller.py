from audio.voice_listener import VoiceListenerThread


def recognize_voice(ui, audio_service, on_text_callback):
    ui.set_listening(True)

    voice_thread = VoiceListenerThread(audio_service)

    def process_text(text: str):
        text = text.replace("venga", "vega")
        text = text.replace("vega", "Vega")

        ui.show_text(f"Pablo: {text}\n")
        on_text_callback(text)

    voice_thread.text_recognized.connect(process_text)
    voice_thread.finished_listening.connect(
        lambda: ui.set_listening(False)
    )

    voice_thread.start()
    return voice_thread
