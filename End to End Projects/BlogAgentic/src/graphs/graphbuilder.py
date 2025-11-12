from langgraph.graph import StateGraph, START, END
from src.llms.groqllm import GroqLLM
from src.nodes.blog_node import BlogNode
from src.states.blog_state import BlogState

class GraphBuilder:
    def __init__(self, llm):
        self.llm = llm
        self.workflow = StateGraph(BlogState)
        
    def build_topic_graph(self):
        """
        Build a graph containing blogs based on the topic
        """
        blog_node_obj = BlogNode(self.llm)
        ## define Nodes
        self.workflow.add_node("title_creation", blog_node_obj.title_creation)
        self.workflow.add_node("content_generation", blog_node_obj.content_generation)
        
        # define edges
        self.workflow.add_edge(START, "title_creation")
        self.workflow.add_edge("title_creation", "content_generation")
        self.workflow.add_edge("content_generation", END)
        
        return self.workflow
    
    def setup_graph(self):
        return self.build_topic_graph().compile()
    
# below code is for langgraph studio
llm = GroqLLM().get_llm()
workflow = GraphBuilder(llm)
graph = workflow.build_topic_graph().compile()