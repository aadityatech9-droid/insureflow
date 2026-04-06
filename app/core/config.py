from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL:str

    SECRET_KEY:str

    ALGORITHM:str="HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES:int=30
    REFRESH_TOKEN_EXPIRE_DAYS:int=7

    REDDIS_URL:str="redis://redis:6379/0"

    APP_ENV:str="development"
    REDIS_URL: str 
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        # This is the key line:
        # Environment variables take priority over .env file
        case_sensitive=False
    )
    
settings=Settings()