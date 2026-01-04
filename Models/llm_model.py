from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate


class VegaLLM:
    def __init__(self, model_name: str = "llama3.2"):
        self.model = OllamaLLM(model=model_name)

        self.chat_prompt_template = """
        Today's date: {date}

        Mandatory instructions:
        {instructions}

        Memory:
        {memory}

        Conversation context:
        {context}

        Answer the following:
        {question}

        Answer:
        """

        self.summary_prompt_template = """
        Follow these instructions:
        {summary_instructions}

        Summarize the following according to the instructions:
        {context}
        """

        self.chat_chain = (
            ChatPromptTemplate.from_template(self.chat_prompt_template)
            | self.model
        )

        self.summary_chain = (
            ChatPromptTemplate.from_template(self.summary_prompt_template)
            | self.model
        )

    def respond(
        self,
        date: str,
        instructions: str,
        memory: str,
        context: str,
        question: str,
    ) -> str:
        if isinstance(memory, list):
            if memory:
                memory_text = "Relevant memory:\n" + "\n".join(
                    f"- {item}" for item in memory
                )
            else:
                memory_text = ""
        else:
            memory_text = memory

        response = self.chat_chain.invoke(
            {
                "date": date,
                "instructions": instructions,
                "memory": memory_text,
                "context": context,
                "question": question,
            }
        )

        if isinstance(response, str):
            return response

        return response.content



    def summarize(
        self,
        summary_instructions: str,
        context: str,
    ) -> str:
        response = self.summary_chain.invoke(
            {
                "summary_instructions": summary_instructions,
                "context": context,
            }
        )

        if isinstance(response, str):
            return response

        return response.content


