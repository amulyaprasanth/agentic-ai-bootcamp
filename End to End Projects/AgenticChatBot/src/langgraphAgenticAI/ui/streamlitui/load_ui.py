import streamlit as st
import os
from src.langgraphAgenticAI.ui.uiconfigfile import Config

class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()
        self.user_controls: dict = {}
        
        
    def load_streamlit_ui(self):
        st.set_page_config(page_title="🤖 " + self.config.get_page_title(), layout="wide")
        st.header("🤖 " + self.config.get_page_title())
        st.session_state.isFetchButtonClicked=False
        with st.sidebar:
            # get options from config
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()
            
            # llm selection
            self.user_controls['selected_llm'] = st.selectbox("Select LLM", llm_options)
            
            if self.user_controls["selected_llm"] == "Groq":
                # model selection
                model_options = self.config.get_groq_model_options()
                
                self.user_controls["selected_groq_model"] = st.selectbox("Select Model", model_options
                                                                         )
                
                self.user_controls["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"] =  st.text_input("API Key", key = "password")
                
                # validate api key
                if not self.user_controls["GROQ_API_KEY"]:
                    st.warning("⚠️ Please enter your GROQ API key to proceed")
            
            # Use Case selectoin
            self.user_controls["selected_usecase"] = st.selectbox("Select Usecases", usecase_options)
            
            if self.user_controls["selected_usecase"].strip() == "Chatbot With Web" or self.user_controls["selected_usecase"].strip() == "AI News":
                os.environ["TAVILY_API_KEY"] = self.user_controls["TAVILY_API_KEY"] = st.session_state["TAVILY_API_KEY"] = st.text_input("Enter your Tavily API Key", type="password")
                
                if not self.user_controls["TAVILY_API_KEY"]:
                    st.warning("⚠️ Please enter your Tavily API key For more info: https://app.tavily.com/home ")
                    
            if self.user_controls["selected_usecase"].strip() == "AI News":
                st.subheader("📅 AI News Explorer")
                
                with st.sidebar:
                    time_frame=st.selectbox(
                        "📆 Select Time Frame",
                        ["Daily", "Weekly", "Monthly"]
                    )

                if st.button("🔍 Fetch Latest AI News", use_container_width=True):
                    st.session_state.isFetchButtonClicked = True
                    st.session_state.timeframe = time_frame 
            
        return self.user_controls