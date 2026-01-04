VEGA
🇬🇧 English
Overview

VEGA is a desktop AI assistant built in Python, developed as a personal and experimental project.

Its main purpose is to explore how a local Large Language Model (LLM) can be integrated into a desktop graphical interface, combining voice interaction, text-based communication, and external services, while preserving a clean and maintainable codebase.

The project focuses on architectural clarity, modularity, and progressive refactoring rather than on delivering a finished or commercial product.

What VEGA Does

VEGA runs a local language model using Ollama and LangChain and exposes it through a desktop application built with PySide6 (Qt).

Interaction can happen either by text or voice. Voice input and audio output are handled asynchronously to keep the interface responsive. Around the core LLM, several independent services are integrated, such as weather queries, media playback, web searches, and messaging.

Contacts and other persistent data are stored locally and can be managed visually from the GUI, without modifying the code.

Project Structure

The codebase is organized to keep responsibilities clearly separated.

The views package contains all user interface components built with PySide6.
The controllers package handles application flow and coordinates interactions between UI, services, and the language model.
The models package contains the LLM integration and memory-related logic.
The services package groups independent features such as weather, playback, messaging, and contact management.

This structure allows the project to grow without accumulating unnecessary coupling or technical debt.

Philosophy

VEGA is intentionally designed as a learning-driven project.

It favors readability, refactoring, and explicit design decisions over speed or feature count. The goal is not to build a finished assistant, but to maintain a solid foundation that can evolve over time as new ideas and improvements are explored.

🇪🇸 Español
Descripción general

VEGA es un asistente de escritorio desarrollado en Python, concebido como un proyecto personal de aprendizaje y experimentación.

Su objetivo principal es explorar cómo integrar un modelo de lenguaje local (LLM) en una interfaz gráfica de escritorio, combinando interacción por voz, comunicación por texto y distintos servicios externos, manteniendo una base de código clara y mantenible.

El proyecto prioriza la arquitectura, la modularidad y la refactorización progresiva frente a la idea de producto terminado.

Qué hace VEGA

VEGA ejecuta un modelo de lenguaje local mediante Ollama y LangChain, integrado en una aplicación de escritorio construida con PySide6 (Qt).

La interacción puede realizarse tanto por texto como por voz. La entrada de audio y la salida por voz se gestionan de forma asíncrona para no bloquear la interfaz. Alrededor del LLM se integran distintos servicios independientes, como consultas meteorológicas, reproducción multimedia, búsquedas web y mensajería.

Los contactos y otros datos persistentes se almacenan localmente y pueden gestionarse de forma visual desde la propia interfaz, sin necesidad de modificar el código.

Estructura del proyecto

El código está organizado para mantener una separación clara de responsabilidades.

El paquete views contiene todos los componentes de la interfaz gráfica desarrollados con PySide6.
El paquete controllers gestiona el flujo de la aplicación y coordina la interacción entre la interfaz, los servicios y el modelo de lenguaje.
El paquete models incluye la integración del LLM y la lógica relacionada con la memoria.
El paquete services agrupa las funcionalidades independientes como el tiempo, la reproducción, la mensajería y la gestión de contactos.

Esta organización facilita la evolución del proyecto sin generar acoplamientos innecesarios.

Filosofía

VEGA está planteado deliberadamente como un proyecto orientado al aprendizaje.

Se da prioridad a la legibilidad del código, a la refactorización y a decisiones de diseño explícitas, por encima de la rapidez o del número de funcionalidades. No se trata de construir un asistente cerrado, sino de mantener una base sólida sobre la que seguir experimentando y mejorando con el tiempo.