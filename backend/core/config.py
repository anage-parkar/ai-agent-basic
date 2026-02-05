from pydantic_settings import BaseSettings
from typing import Optional, List



class Settings(BaseSettings):
    # LLM Configuration
    llm_provider: str = "ollama"  # openai, hf, ollama
    
    # OpenAI
    # openai_api_key: Optional[str] = None
    # openai_model: str = "gpt-4"
    
    # Hugging Face
    huggingface_api_key: Optional[str] = None
    huggingface_model: str = "meta-llama/Llama-2-70b-chat-hf"
    
    # Ollama
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2:latest"
    
    # MongoDB
    mongo_uri: str = "mongodb://localhost:27017"
    mongo_db: str = "analytics"
    
    # Azure Bing Search
    azure_bing_search_key: Optional[str] = None
    azure_bing_search_endpoint: str = "https://api.bing.microsoft.com/v7.0/search"
    
    # CORS
    allow_origins: str = "http://localhost:5173,http://localhost:3000"
    
    # Agent Settings
    max_iterations: int = 5
    agent_temperature: float = 0.7
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    @property
    def origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.allow_origins.split(",")]


settings = Settings()
