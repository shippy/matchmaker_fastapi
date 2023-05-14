from dotenv import load_dotenv
from dataclasses import dataclass
import os

_ = load_dotenv()

@dataclass(frozen=True)
class Settings:
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 3
    SECRET_KEY = os.environ["SECRET_KEY"]
    
    
settings = Settings()