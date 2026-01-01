#LLMs
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate


class VegaLLM:
    def __init__(self, model_name: str = "llama3.2"):
        self.model = OllamaLLM(model=model_name)

        self.plantilla_chat = """
        Fecha de hoy: {fecha}

        Instrucciones obligatorias:
        {instrucciones}

        Memoria:
        {memoria}

        Topic de conversación:
        {context}

        Responde lo siguiente:
        {question}

        Respuesta:
        """

        self.plantilla_resumen = """
        Sigue estas instrucciones:
        {instrucciones_resumen}
        Resume esto siguiendo las instrucciones:
        {context}
        """

        self.chain_chat = (
            ChatPromptTemplate.from_template(self.plantilla_chat)
            | self.model
        )

        self.chain_resumen = (
            ChatPromptTemplate.from_template(self.plantilla_resumen)
            | self.model
        )

    def responder(
        self,
        fecha: str,
        instrucciones: str,
        memoria: str,
        context: str,
        question: str,
    ) -> str:
        return self.chain_chat.invoke(
            {
                "fecha": fecha,
                "instrucciones": instrucciones,
                "memoria": memoria,
                "context": context,
                "question": question,
            }
        )

    def resumir(
        self,
        instrucciones_resumen: str,
        context: str,
    ) -> str:
        return self.chain_resumen.invoke(
            {
                "instrucciones_resumen": instrucciones_resumen,
                "context": context,
            }
        )