import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class LLMConfig:
    api_key: str
    model: str = "llama-3.1-70b-versatile"

class Config:
    def __init__(self):
        self.default_api_key = os.getenv("GROQ_API_KEY", "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")
        self.llm_configs = {
            "default": LLMConfig(api_key=self.default_api_key)
        }
    
    def get_llm_config(self, config_name: str = "default") -> Optional[LLMConfig]:
        return self.llm_configs.get(config_name)

config = Config()