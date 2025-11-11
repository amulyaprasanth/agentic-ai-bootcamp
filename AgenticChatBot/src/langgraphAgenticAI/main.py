import streamlit as st

from src.langgraphAgenticAI.graph.graph_builder import GraphBuilder
from src.langgraphAgenticAI.ui.streamlitui.load_ui import LoadStreamlitUI
from src.langgraphAgenticAI.LLMs.groqllm import GroqLLM
from src.langgraphAgenticAI.ui.streamlitui.display_result import DisplayResultStreamlit


def load_langgraph_agenticai_app():
    """Loads and runs the appliction with Streamlit UI. this functions initialized an UI.
    """
    
    # load ui
    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()
    
    if not user_input:
        st.error("Error: Failed to load user input from UI.")
        
    
    user_message = st.chat_input("Enter your message: ")
    
    if user_message:
        try:
            # configure llms
            obj_llm_config = GroqLLM(user_input)
            model = obj_llm_config.get_llm_model()
            
            if not model:
                st.error("Error: LLM model could not be initialized")
                return
                
            # initilaize and setup graph as per usecase
            use_case = user_input.get("selected_usecase")
            
            if not use_case:
                st.error("Error: No use case selected")
                return
            
            # graph builder
            graph_builder = GraphBuilder(model)
            
            try:
                graph = graph_builder.setup_graph(use_case)
                DisplayResultStreamlit(use_case, graph, user_message).display_results_on_ui()
                
            except Exception as e:
                st.error(f"Error graph setup failed: {e}")
                return
            
            
        except Exception as e:
            st.error(f"Error Loading Graph: {e}")