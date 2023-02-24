import dataclasses
import dotenv
import os


@dataclasses.dataclass
class Secrets:
    """.env file structure"""

    OPENAI_API_KEY: str
    TELEGRAM_API_KEY: str


def load_secrets() -> Secrets:
    """Return .env params (Secrets DataClass)"""
    dotenv.load_dotenv()
    return Secrets(
        OPENAI_API_KEY=os.getenv("OPENAI_API_KEY"),
        TELEGRAM_API_KEY=os.getenv("TELEGRAM_API_KEY"),
    )
