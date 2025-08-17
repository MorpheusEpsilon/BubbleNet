import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILIO_PHONE_NUMBER: str
    PARENT_PHONE: str
    BLACKLIST: list[str] = ["phishing", "malware", "kaotic"]

    class Config:
        env_file = ".env"

settings = Settings()
