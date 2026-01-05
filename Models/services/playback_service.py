# PABLO BOTELLA JIMÉNEZ
# Vega AI Assistant Application

# Provides YouTube playback functionality for the Vega AI assistant.
# Uses the pywhatkit library to play YouTube videos based on user queries.


# LIBRARY IMPORTS
import pywhatkit


def play_youtube(query):
    if not query:
        return None

    pywhatkit.playonyt(query)
    return f"Reproduciendo {query}"
