import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from typing import ClassVar, List

load_dotenv()

class Settings(BaseSettings):
    class Config:
        env_file = ".env"
    
    # APP SETTINGS
    APP_VERSION: str = '0.1.0'
    APP_PORT: int = 8000
    APP_HOST: str = "0.0.0.0"
    APP_ROOT_PATH: str = ''
    
    # SECURITY SETTINGS
    API_KEY: str = os.getenv('API_KEY', 'your-super-secret-key')  
    API_KEY_NAME: str = "Authorization"
    
    # API Settings
    CORS_ORIGINS: List[str] = ["*"]  # In production, replace with specific origins
    API_VERSION: str = "1.0.0"
    API_TITLE: str = "ETL AI Pipeline"
    API_DESCRIPTION: str = "ETL AI Pipeline for AI research"

    # SUPABASE SETTINGS
    SUPABASE_URL: str = os.getenv('SUPABASE_URL')
    SUPABASE_SERVICE_KEY: str = os.getenv('SUPABASE_SERVICE_KEY')
    MAX_CONNECTIONS: int = 10

    # Logging Settings
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    # ANTHROPIC SETTINGS
    ANTHROPIC_API_KEY: str = os.getenv('ANTHROPIC_API_KEY')

    # POLYGON SETTINGS
    POLYGON_API_KEY: str = os.getenv('POLYGON_API_KEY')

settings = Settings()

if __name__ == '__main__':
    print(f"APP_VERSION: {settings.APP_VERSION}")
    print(f"APP_PORT: {settings.APP_PORT}")
    print(f"APP_HOST: {settings.APP_HOST}")
    print(f"API_KEY: {settings.API_KEY}")
