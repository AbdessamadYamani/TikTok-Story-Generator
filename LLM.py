from typing import Optional
from langchain_groq import ChatGroq
from config import config

class StoryProcessor:
    def __init__(self, config_name: str = "default"):
        llm_config = config.get_llm_config(config_name)
        if not llm_config:
            raise ValueError(f"Configuration '{config_name}' not found")
        
        self.llm = ChatGroq(
            api_key=llm_config.api_key,
            model=llm_config.model
        )
    
    def get_llm_response(self, input_text: str) -> str:
        try:
            Intro="The following stoty is for a tiktok video , re-create it like it happend to you in a 1 minute video, make it interesting as a story to hear"
            response = self.llm.invoke(Intro+input_text)
            return response.content
        except Exception as e:
            raise RuntimeError(f"Error getting LLM response: {str(e)}")
    
    def get_story_title(self, story: str) -> str:
        prompt = "Create a title for this story with 4 words maximum:\n\n"
        return self.get_llm_response(prompt + story)
    
    def get_story_summary(self, story: str) -> str:
        prompt = """Create a summary for this story in 3 phrases maximum, 
        it should be creative to get people's attention:\n\n"""
        return self.get_llm_response(prompt + story)