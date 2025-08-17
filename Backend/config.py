#Key handling from the .env
from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    OPENAI_API_KEY: str | None
    TWILIO_ACCOUNT_SID: str | None
    TWILIO_AUTH_TOKEN: str | None
    TWILIO_PHONE_NUMBER: str | None
    PARENT_PHONE: str | None
    BLACKLIST: list[str]

settings = Settings(
    OPENAI_API_KEY=os.getenv("OPENAI_API_KEY"),
    TWILIO_ACCOUNT_SID=os.getenv("TWILIO_ACCOUNT_SID"),
    TWILIO_AUTH_TOKEN=os.getenv("TWILIO_AUTH_TOKEN"),
    TWILIO_PHONE_NUMBER=os.getenv("TWILIO_PHONE_NUMBER"),
    PARENT_PHONE=os.getenv("PARENT_PHONE"),
    BLACKLIST=["phishing", "malware", "kaotic"]             #Only for development/ Hard Blacklist
)
