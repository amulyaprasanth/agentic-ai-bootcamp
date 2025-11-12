from langgraph.graph import StateGraph, START, END
from src.langgraphAgenticAI.state.state import State
from src.langgraphAgenticAI.nodes.basic_chatbot_node import BasicChatBotNode
from src.langgraphAgenticAI.tools.web_search_tool import Tools
from src.langgraphAgenticAI.nodes.chatbot_with_tools_node import ChatbotWithToolNode
from langgraph.prebuilt.tool_node import tools_condition
from src.langgraphAgenticAI.nodes.ai_news_node import AINewsNode
class GraphBuilder:
    def __init__(self, model):
        self.llm = model
        self.graph_builder = StateGraph(State)
        
        
    def basic_chatbot_build_graph(self):
        """
        Building a basic chatbot graph using langGraph.
        """
        self.basic_chatbot_node = BasicChatBotNode(model = self.llm)
        self.graph_builder.add_node("chatbot", self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_edge("chatbot", END)
        
    def chatbot_with_tools_graph(self):
        """ 
        Building a Chatbot with tools using langGraph
        """
        
        # define tools and tool node
        tools = Tools()
        external_tools = tools.get_tools()
        tool_node = tools.create_tool_node(external_tools)
        
        # define llm
        llm = self.llm
        
        obj_chatbot_with_tools = ChatbotWithToolNode(llm)
        chatbot = obj_chatbot_with_tools.create_chatbot(external_tools)
        
        self.graph_builder.add_node("chatbot", chatbot)
        self.graph_builder.add_node("tools", tool_node)
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_conditional_edges("chatbot", tools_condition)
        self.graph_builder.add_edge("tools", "chatbot")       
        
    def ai_news_builder_graph(self):
        
        ai_news_node = AINewsNode(self.llm)
        self.graph_builder.add_node("fetch_news", ai_news_node.fetch_news) # type:ignore
        self.graph_builder.add_node("summarize_news", ai_news_node.summarize_news)# type:ignore
        self.graph_builder.add_node("save_results", ai_news_node.save_results)# type:ignore
        
        
        self.graph_builder.add_edge(START, "fetch_news")
        self.graph_builder.add_edge("fetch_news", "summarize_news")
        self.graph_builder.add_edge("summarize_news", "save_results")
        self.graph_builder.add_edge("save_results", END)

    def setup_graph(self, usecase: str):
        """
        Sets up the graph for selected use case
        """
        
        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()
            
        if usecase == "Chatbot With Web":
            self.chatbot_with_tools_graph()
            
        if usecase == "AI News":
            self.ai_news_builder_graph()
            
        return self.graph_builder.compile()