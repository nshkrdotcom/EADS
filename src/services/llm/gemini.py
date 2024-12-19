"""Gemini model integration using LangChain."""

from typing import Any, List, Optional

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI


class GeminiService:
    """Service class for interacting with Google's Gemini model."""

    def __init__(self, api_key: str, model_name: str = "gemini-pro") -> None:
        """Initialize the Gemini service.

        Args:
            api_key: Google API key for accessing Gemini
            model_name: Name of the Gemini model to use
        """
        self.model = ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=api_key,
            temperature=0.7,
            convert_system_message_to_human=True,
        )
        self.output_parser = StrOutputParser()

    def create_chat_prompt(
        self, system_message: Optional[str] = None
    ) -> ChatPromptTemplate:
        """Create a chat prompt template.

        Args:
            system_message: Optional system message to set context

        Returns:
            ChatPromptTemplate configured with system and human messages
        """
        messages = []
        if system_message:
            messages.append(SystemMessage(content=system_message))

        messages.extend(
            [
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessage(content="{input}"),
            ]
        )

        return ChatPromptTemplate.from_messages(messages)

    async def generate_response(
        self,
        prompt: str,
        system_message: Optional[str] = None,
        chat_history: Optional[List[Any]] = None,
    ) -> str:
        """Generate a response using the Gemini model.

        Args:
            prompt: User input prompt
            system_message: Optional system message for context
            chat_history: Optional list of previous messages

        Returns:
            str: Generated response from Gemini
        """
        chat_prompt = self.create_chat_prompt(system_message)
        chain = chat_prompt | self.model | self.output_parser

        response: str = await chain.ainvoke(
            {"input": prompt, "chat_history": chat_history or []}
        )

        return response
