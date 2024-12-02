from pydantic_settings  import BaseSettings

class Settings(BaseSettings):
    CREATE_ADMIN_USERNAME : str 
    CREATE_ADMIN_EMAIL : str 
    CREATE_ADMIN_PASSWORD : str 
    CREATE_ADMIN_ROL : str 
    DATABASE_URL: str
    ADMIN_USERNAME: str
    debug: bool = False

    CLOUD_NAME:str
    CLOUD_KEY:str
    CLOUD_SECRET:str

    class Config:
        env_file = ".env"  

settings = Settings()