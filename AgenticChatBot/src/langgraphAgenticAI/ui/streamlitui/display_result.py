import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage


class DisplayResultStreamlit:
    def __init__(self, usecase, graph, user_message):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message

    def display_results_on_ui(self):
        """Main entry point to handle different use cases."""
        handlers = {
            "Basic Chatbot": self._handle_basic_chatbot,
            "Chatbot With Web": self._handle_chatbot_with_web,
            "AI News": self._handle_ai_news
        }

        handler = handlers.get(self.usecase)
        if handler:
            handler()
        else:
            st.error(f"Unsupported usecase: {self.usecase}")

    # ------------------------------------------------------------------------
    # 🧠 Helper Methods
    # ------------------------------------------------------------------------

    def _display_user_message(self, message: str):
        with st.chat_message("user"):
            st.write(message)

    def _handle_basic_chatbot(self):
        """Handles the Basic Chatbot usecase."""
        self._display_user_message(self.user_message)

        with st.spinner("Assistant is thinking..."):
            for event in self.graph.stream({"messages": ("user", self.user_message)}):
                for value in event.values():
                    ai_message = value.get("messages")
                    if ai_message:
                        with st.chat_message("assistant"):
                            st.write(ai_message.content)

    def _handle_chatbot_with_web(self):
        """Handles Chatbot with Web usecase."""
        self._display_user_message(self.user_message)

        with st.spinner("Assistant is thinking..."):
            res = self.graph.invoke({"messages": [self.user_message]})

        self._display_chatbot_responses(res.get('messages', []))

    def _display_chatbot_responses(self, messages):
        """Displays messages from AI or tools."""
        for message in messages:
            if isinstance(message, HumanMessage):
                self._display_user_message(message.content) # type:ignore
            elif isinstance(message, ToolMessage):
                with st.expander("Tool calls"):
                    st.write(message.content)
            elif isinstance(message, AIMessage) and message.content:
                with st.chat_message("assistant"):
                    st.write(message.content)

    def _handle_ai_news(self):
        """Handles AI News usecase."""
        frequency = self.user_message
        ai_news_path = f"./AINews/{frequency.lower()}_summary.md"

        with st.spinner("Analyzing News...⌛⌛"):
            self.graph.invoke({"messages": frequency})
            self._display_news_file(ai_news_path)

    def _display_news_file(self, file_path: str):
        """Reads and displays the markdown file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                markdown_content = file.read()
            st.markdown(markdown_content, unsafe_allow_html=True)
        except FileNotFoundError:
            st.error(f"News not generated or file not found: {file_path}")
        except Exception as e:
            st.error(f"An Error occurred: {str(e)}")
