from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from pydantic import SecretStr

class GroqLLM:
    def __init__(self):
        load_dotenv()
        
    def get_llm(self):
        try:
            groq_api_key = SecretStr(os.getenv("GROQ_API_KEY", ""))
            llm = ChatGroq(api_key=groq_api_key, model="openai/gpt-oss-20b")
            return llm
        
        except Exception as e:
            raise ValueError(f"Error occurred initializing llm with Exception: {e}")