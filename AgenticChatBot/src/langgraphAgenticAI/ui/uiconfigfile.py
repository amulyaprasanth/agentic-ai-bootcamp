from configparser import ConfigParser

class Config:
    def __init__(self, config_file="./src/langgraphAgenticAI/ui/uiconfig.ini"):
        self.configuration = ConfigParser()
        self.configuration.read(config_file)
        
    def get_llm_options(self):
        return self.configuration["DEFAULT"].get("LLM_OPTIONS", "").split(", ")
        
    def get_usecase_options(self):
        return self.configuration["DEFAULT"].get("USECASE_OPTIONS", "").split(", ")
    
    def get_groq_model_options(self):
        return self.configuration["DEFAULT"].get("GROQ_MODEL_OPTIONS", "").split(", ")
    
    def get_page_title(self):
        return self.configuration['DEFAULT'].get("PAGE_TITLE", "")