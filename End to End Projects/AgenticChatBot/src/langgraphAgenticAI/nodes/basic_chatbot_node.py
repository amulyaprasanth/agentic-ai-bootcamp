

from src.langgraphAgenticAI.state.state import State

class BasicChatBotNode:
    """
    Basic chatbot Login implementation
    """
    def __init__(self, model):
        self.llm = model
        
    def process(self, state:State) :
        """
        Processes the input state and generates a chatbot message 
        """
        
        return {"messages": self.llm.invoke(state["messages"])}