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
        return self.chat_chain.invoke(
            {
                "date": date,
                "instructions": instructions,
                "memory": memory,
                "context": context,
                "question": question,
            }
        )

    def summarize(
        self,
        summary_instructions: str,
        context: str,
    ) -> str:
        return self.summary_chain.invoke(
            {
                "summary_instructions": summary_instructions,
                "context": context,
            }
        )
