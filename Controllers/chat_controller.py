from unidecode import unidecode

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
):
    normalized_input = user_input.lower()
    context = context_holder["context"]

    # Load memory and instructions
    instructions = memory.read_instructions(assets_text)
    instructions_summary = memory.read_instructions_summary(assets_text)
    memory_text = memory.read_memory(assets_text)

    # Search
    if "search" in normalized_input:
        for provider in SEARCH_PROVIDERS:
            if provider in normalized_input:
                query = clean_search_query(user_input, provider)
                result = search(provider, query)

                if result:
                    ui.show_text(f"Vega: {result}\n")
                    audio_service.speak(result)
                return

    # Play media
    if "play" in normalized_input:
        query = (
            normalized_input
            .replace("vega", "")
            .replace("play", "")
            .strip()
        )

        result = play_youtube(query)

        if result:
            ui.show_text(f"Vega: {result}\n")
            audio_service.speak(result)
        return

    # Weather
    if "weather" in normalized_input:
        for city in cities:
            if city in normalized_input:
                data = get_weather(city)

                if data:
                    ui.show_text(f"Vega: Weather in {city}:\n")
                    audio_service.speak(f"Weather in {city}")
                    for line in data:
                        ui.show_text(f"{line}\n")
                else:
                    ui.show_text(
                        f"Vega: Unable to get weather for {city}\n"
                    )
                    audio_service.speak(
                        f"Unable to get weather for {city}"
                    )
                return

    # Messaging
    if "send" in normalized_input:
        for contact in contacts:
            if contact in normalized_input:
                message = None
                triggers = ["that ", "saying ", "message "]

                for trigger in triggers:
                    if trigger in normalized_input:
                        message = normalized_input.split(trigger, 1)[1].strip()
                        break

                if not message:
                    audio_service.speak(
                        f"What message do you want to send to {contact}?"
                    )
                    ui.show_text(
                        f"\nVega: What message do you want to send to {contact}?\n"
                    )
                    message = audio_service.listen()

                    if not message:
                        audio_service.speak("I didn't understand you")
                        ui.show_text(
                            "Vega: I didn't understand you\n"
                        )
                        return

                sent = send_whatsapp(contacts[contact], message)

                if sent:
                    audio_service.speak(
                        f"Message sent to {contact}"
                    )
                    ui.show_text(
                        f"Vega: Message sent to {contact}\n"
                    )
                else:
                    audio_service.speak(
                        "Unable to send the message"
                    )
                    ui.show_text(
                        "Vega: Unable to send the message\n"
                    )
                return

    # Cut / summarize
    if "cut" in normalized_input:
        summary = llm.summarize(instructions_summary, context)
        summary = unidecode(summary)

        memory.save_summary(assets_text, summary)

        ui.show_text(
            "\nVega: Summary saved to memory.\n"
        )
        audio_service.speak(
            "Summary saved to memory."
        )
        return

    # Normal conversation
    if context is None:
        context = ""

    result = llm.respond(
        current_date,
        instructions,
        memory_text,
        context,
        user_input,
    )
    result = unidecode(result)

    ui.show_text(f"\nVega: {result}\n")
    audio_service.speak(result)

    context += f"Pablo: {user_input}\nVega: {result}\n"
    context_holder["context"] = context
