# VEGA

## Overview

VEGA is a desktop AI assistant developed in Python as a personal and experimental project.

Its purpose is to explore the integration of a **local Large Language Model (LLM)** into a desktop graphical application, combining text interaction, voice input/output, and independent services, while keeping a clear and maintainable architecture.

VEGA is not intended as a finished product. It is a learning-oriented project focused on structure, refactoring, and design decisions.

---

## Core Technologies

- Python
- PySide6 (Qt) for the graphical interface
- Ollama for running local language models
- LangChain for LLM integration
- SpeechRecognition and pyttsx3 for voice interaction

---

## Functionality

VEGA exposes a local LLM through a desktop application.

Interaction modes:
- text-based chat
- voice input with spoken responses

Around the LLM, several independent services are integrated, such as:
- weather queries
- media playback
- web searches
- messaging and contact management

All data is stored locally. Persistent information can be managed from the GUI without modifying the source code.

---

## Project Structure

The codebase follows a modular structure with clear responsibility boundaries:

- views  
  user interface components built with PySide6

- controllers  
  application flow and coordination between UI, services and the LLM

- models  
  LLM integration and memory-related logic

- services  
  independent features such as weather, messaging or playback

This structure is designed to allow growth without unnecessary coupling.

---

## Design Principles

- clarity over cleverness  
- explicit architecture decisions  
- modular and refactor-friendly code  
- learning and experimentation over feature completeness

VEGA prioritizes maintainability and readability over speed or scope.

---

## Notes

VEGA is intentionally local-first and experimental.

Its value lies in the architectural exploration and the evolution of the codebase, not in delivering a commercial-grade assistant.



# VEGA

## Descripción general

VEGA es un asistente de escritorio desarrollado en Python como un proyecto personal y experimental.

Su propósito es explorar la integración de un **modelo de lenguaje local (LLM)** en una aplicación gráfica de escritorio, combinando interacción por texto, entrada y salida por voz, y servicios independientes, manteniendo una arquitectura clara y mantenible.

VEGA no está concebido como un producto terminado. Es un proyecto orientado al aprendizaje, centrado en la estructura, la refactorización y las decisiones de diseño.

---

## Tecnologías principales

- Python
- PySide6 (Qt) para la interfaz gráfica
- Ollama para la ejecución de modelos de lenguaje locales
- LangChain para la integración del LLM
- SpeechRecognition y pyttsx3 para la interacción por voz

---

## Funcionalidad

VEGA expone un modelo de lenguaje local a través de una aplicación de escritorio.

Modos de interacción:
- chat por texto
- entrada por voz con respuestas habladas

Alrededor del LLM se integran distintos servicios independientes, como:
- consultas meteorológicas
- reproducción multimedia
- búsquedas web
- mensajería y gestión de contactos

Toda la información se almacena localmente. Los datos persistentes pueden gestionarse desde la interfaz gráfica sin modificar el código fuente.

---

## Estructura del proyecto

La base de código sigue una estructura modular con responsabilidades bien definidas:

- views  
  componentes de la interfaz gráfica desarrollados con PySide6

- controllers  
  control del flujo de la aplicación y coordinación entre la interfaz, los servicios y el LLM

- models  
  integración del LLM y lógica relacionada con la memoria

- services  
  funcionalidades independientes como tiempo, mensajería o reproducción

Esta estructura está pensada para permitir la evolución del proyecto sin generar acoplamientos innecesarios.

---

## Principios de diseño

- claridad frente a ingenio  
- decisiones arquitectónicas explícitas  
- código modular y fácil de refactorizar  
- aprendizaje y experimentación por encima de la completitud funcional

VEGA prioriza la mantenibilidad y la legibilidad frente a la rapidez o al alcance de funcionalidades.

---

## Notas

VEGA es intencionadamente local y experimental.

Su valor reside en la exploración arquitectónica y en la evolución de la base de código, no en la entrega de un asistente de nivel comercial.




# NAMING CONVENTIONS

## VEGA – Naming Conventions
=========================

This document describes the naming conventions used consistently
throughout the VEGA project.

The goal of these conventions is to ensure clarity, consistency,
and maintainability across the entire codebase.


1. General rules
----------------

- All code, identifiers, and comments are written in English.
- Naming is explicit and descriptive; abbreviations are avoided unless
  they are widely accepted.
- Consistency is preferred over cleverness.


2. Directories and files
------------------------

- Directories use snake_case.
- Python files use snake_case.

Examples:
- main.py
- main_window.py
- chat_controller.py
- contacts_service.py
- assets_images/
- assets_text/


3. Classes
----------

- Class names use CamelCase.
- Class names are nouns and describe a single responsibility.

Examples:
- VegaUI
- VegaLLM
- AddContactDialog
- AudioService


4. Functions and methods
------------------------

- Function and method names use snake_case.
- Names are verbs or verb phrases describing the action performed.

Examples:
- handle_chat
- recognize_voice
- get_contacts
- add_contact
- delete_contact
- load_contacts


5. Variables
------------

- Variable names use snake_case.
- Names are descriptive and avoid single-letter identifiers
  except in very limited scopes.

Examples:
- audio_service
- current_date
- contacts_list
- phone_number
- assets_text


6. Constants
------------

- Constants use UPPER_SNAKE_CASE.
- Constants are defined at module level.

Examples:
- ASSETS_IMAGES
- ASSETS_TEXT
- CITIES


7. Services
-----------

- Service modules are named using snake_case and end with _service
  when appropriate.
- Services expose clear, stateless functions and do not depend on UI.

Examples:
- contacts_service.py
- weather_service.py
- messaging_service.py


8. User Interface
-----------------

- UI classes follow CamelCase.
- UI-related logic is kept inside view classes.
- Business logic and persistence are handled outside the UI layer.


9. Language separation
----------------------

- Code identifiers are always in English.
- User-facing strings may be localized (e.g. Spanish),
  but logic and naming remain in English.


10. Philosophy
--------------

These conventions are intentionally simple.

They are designed to:
- reduce cognitive load,
- avoid ambiguity,
- make refactoring easier,
- and keep the project readable over time.

Consistency across the project takes precedence over external style guides.
