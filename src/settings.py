from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

env_path = Path(__file__).parent.parent / ".env"

# Load environment variables from a .env file if it exists
load_dotenv(env_path)


class Settings(BaseSettings):
    # Jira settings
    JIRA_API_KEY: str = "your_jira_api_key"
    JIRA_BASE_URL: str = "https://your-jira-instance.atlassian.net"
    JIRA_PROJECT_KEY: str = "PROJ"

    # Bitbucket settings
    BITBUCKET_API_KEY: str = "your_bitbucket_api_key"
    BITBUCKET_BASE_URL: str = "https://bitbucket.org"
    BITBUCKET_PROJECT_KEY: str = "PROJ"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
