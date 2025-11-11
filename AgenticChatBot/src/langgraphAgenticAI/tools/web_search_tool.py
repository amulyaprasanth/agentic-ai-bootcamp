from langchain_tavily.tavily_search import TavilySearch
from langgraph.prebuilt import ToolNode

class Tools:
    def __init__(self, max_results: int = 2):
        self.web_search = TavilySearch(max_results=max_results)
        
        
    def get_tools(self):
        """ Returns a list of tools """
        return [self.web_search]
    
    
    def create_tool_node(self, tools):
        """ Create a tool node from list of tools """
        return ToolNode(tools)
    