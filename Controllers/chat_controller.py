# LIBRS IMPORTS
from unidecode import unidecode
import json

# FILE IMPORTS
from models import memory
from models.services.search_service import (
    SEARCH_PROVIDERS,
    clean_search_query,
    search,
)
from models.services.playback_service import play_youtube
from models.services.weather_service import get_weather
from models.services.messaging_service import send_whatsapp

def handle_chat(
    user_input,
    ui,
    audio_service,
    llm,
    contacts,
    cities,
    assets_text,
    current_date,
    context_holder,
    intent_classifier,
    memory_manager,
    ):
    normalized_input = user_input.lower()
    context = context_holder["context"]

    # Load system instructions (only system prompt)
    instructions = memory.read_instructions(assets_text)

    # Search
    if "busca" in normalized_input:
        for provider in SEARCH_PROVIDERS:
            if provider in normalized_input:
                query = clean_search_query(user_input, provider)
                result = search(provider, query)

                if result:
                    ui.show_text(f"Vega: {result}\n")
                    audio_service.speak(result)
                return

    # Play media
    if "reproduce" in normalized_input:
        query = (
            normalized_input
            .replace("vega", "")
            .replace("reproduce", "")
            .strip()
        )

        result = play_youtube(query)

        if result:
            ui.show_text(f"Vega: {result}\n")
            audio_service.speak(result)
        return

    # Weather
    if "tiempo hace" in normalized_input:
        for city in cities:
            if city in normalized_input:
                data = get_weather(city)

                if data:
                    ui.show_text(f"Vega: El tiempo en {city} es este:\n")
                    audio_service.speak(f"El tiempo en {city} es este")
                    for line in data:
                        ui.show_text(f"{line}\n")
                else:
                    ui.show_text(
                        f"Vega: No he podido obtener el tiempo de {city}\n"
                    )
                    audio_service.speak(
                        f"No he podido obtener el tiempo de {city}"
                    )
                return

    # Messaging
    if "envía" in normalized_input or "envia" in normalized_input:
        for contact in contacts:
            if contact in normalized_input:
                message = None
                triggers = ["que ", "diciendo ", "mensaje "]

                for trigger in triggers:
                    if trigger in normalized_input:
                        message = normalized_input.split(trigger, 1)[1].strip()
                        break

                if not message:
                    audio_service.speak(
                        f"¿Qué mensaje quieres enviar a {contact}?"
                    )
                    ui.show_text(
                        f"\nVega: ¿Qué mensaje quieres enviar a {contact}?\n"
                    )
                    message = audio_service.listen()

                    if not message:
                        audio_service.speak("No te he entendido")
                        ui.show_text(
                            "Vega: No te he entendido\n"
                        )
                        return

                sent = send_whatsapp(contacts[contact], message)

                if sent:
                    audio_service.speak(
                        f"Mensaje enviado a {contact}"
                    )
                    ui.show_text(
                        f"Vega: Mensaje enviado a {contact}\n"
                    )
                else:
                    audio_service.speak(
                        "No he podido enviar el mensaje"
                    )
                    ui.show_text(
                        "Vega: No he podido enviar el mensaje\n"
                    )
                return

    # Manual memory snapshot (legacy, controlled)
    if "corta" in normalized_input:
        if context is None:
            context = ""

        instructions_summary = memory.read_instructions_summary(assets_text)

        summary = llm.summarize(instructions_summary, context)
        summary = unidecode(summary)

        memory.save_summary(assets_text, summary)

        ui.show_text("\nVega: Resumen guardado en memoria.\n")
        audio_service.speak("Resumen guardado en memoria.")
        return

    # Normal conversation (LEVEL 2 FLOW)
    if context is None:
        context = ""

    intent = intent_classifier.classify(user_input)
    relevant_memory = memory_manager.get_relevant_memory(intent)

    result = llm.respond(
        current_date,
        instructions,
        relevant_memory,
        context,
        user_input,
    )

    result = unidecode(result)

    ui.show_text(f"\nVega: {result}\n")
    audio_service.speak(result)

    # ---- MEMORY PROPOSAL (LEVEL 2 WRITE) ----
    memory_proposal_instructions = (
        assets_text / "instructions_memory_proposal.txt"
    ).read_text(encoding="utf-8")

    proposal_raw = llm.summarize(
        memory_proposal_instructions,
        context + f"Pablo: {user_input}\nVega: {result}\n"
    )

    try:
        proposal = json.loads(proposal_raw)
        memory_manager.apply_memory_updates(proposal)
    except Exception:
        pass
    # ----------------------------------------

    context += f"Pablo: {user_input}\nVega: {result}\n"
    context_holder["context"] = context
