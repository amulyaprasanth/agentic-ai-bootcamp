import streamlit as st

from src.langgraphAgenticAI.graph.graph_builder import GraphBuilder
from src.langgraphAgenticAI.ui.streamlitui.load_ui import LoadStreamlitUI
from src.langgraphAgenticAI.LLMs.groqllm import GroqLLM
from src.langgraphAgenticAI.ui.streamlitui.display_result import DisplayResultStreamlit


def load_langgraph_agenticai_app():
    """Loads and runs the application with Streamlit UI."""
    
    # Load UI inputs (like selected usecase)
    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()
    
    if not user_input:
        st.error("Error: Failed to load user input from UI.")
        return

    use_case = user_input.get("selected_usecase")

    # If AI News use case — use the button state instead of chat input
    if use_case == "AI News":
        if st.session_state.get("isFetchButtonClicked", False):
            user_message = st.session_state.get("timeframe", "")
        else:
            st.info("Click the **Fetch News** button to generate AI news.")
            return
    else:
        # For all other use cases — show chat input
        user_message = st.chat_input("Enter your message")

    if not user_message:
        return

    try:
        # Configure LLM
        obj_llm_config = GroqLLM(user_input)
        model = obj_llm_config.get_llm_model()
        
        if not model:
            st.error("Error: LLM model could not be initialized")
            return

        # Build graph
        graph_builder = GraphBuilder(model)

        try:
            graph = graph_builder.setup_graph(use_case)
            DisplayResultStreamlit(use_case, graph, user_message).display_results_on_ui()
        
        except Exception as e:
            import traceback
            st.error(f"Error graph setup failed: {repr(e)}")
            st.code(traceback.format_exc())

    except Exception as e:
        import traceback
        st.error(f"Error Loading Graph: {repr(e)}")
        st.code(traceback.format_exc())
