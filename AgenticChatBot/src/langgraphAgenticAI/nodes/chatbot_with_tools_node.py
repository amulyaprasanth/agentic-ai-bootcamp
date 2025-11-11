from src.langgraphAgenticAI.state.state import State

class ChatbotWithToolNode:
    """
    Chatbot logic enhanced with tool integration.
    """
    
    def __init__(self, model):
        self.llm = model
        
    def process(self, state: State):
        """
        Process the input state and generates a response  with tool integration.

        Args:
            state (State): The current graph state
        """
        
        user_message = state["messages"][-1] if state["messages"] else ""
        llm_response = self.llm.invoke([{"role": "user", "content": user_message}])
        
        return {"messages": [llm_response]}
    
    
    def create_chatbot(self, tools):
        """Returns a chatbot node function

        Args:
            tools (list): list of tools
        """
        llm_with_tools = self.llm.bind_tools(tools)
        
        def create_chatbot_node(state:State):
            """
            Chatbot logic for processing the input staten ahd returning a response
            """
            
            return {"messages": [llm_with_tools.invoke(state["messages"])]}
        
        return  create_chatbot_node