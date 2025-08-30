import os

from pydantic_settings import BaseSettings
from dotenv import load_dotenv


load_dotenv()


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Attributes:
        fastapi_title (str): Title for FastAPI docs.
        fastapi_description (str): Description for FastAPI docs.
        db_dialect (str): Database dialect for SQLAlchemy.
        db_driver (str): Database driver for SQLAlchemy.
        db_user (str): Database username.
        db_password (str): Database password.
        db_host (str): Database host.
        db_port (str): Database port.
        db_name (str): Database name.
        local_db_url (str): URL for local SQLite database
            - (used in debug mode).
        debug (bool): Debug mode flag.
            - If True, use SQLite; otherwise, use production DB.
    """

    fastapi_title: str = os.getenv('FASTAPI_TITLE', 'Issue_manager')
    fastapi_description: str = os.getenv('FASTAPI_DESCRIPTION', '')
    db_dialect: str = os.getenv('DB_DIALECT', 'postgresql')
    db_driver: str = os.getenv('DB_DRIVER', 'asyncpg')
    db_user: str = os.getenv('DB_USER', 'user')
    db_password: str = os.getenv('DB_PASSWORD', 'password')
    db_host: str = os.getenv('DB_HOST', 'db')
    db_port: str = os.getenv('DB_PORT', '5432')
    db_name: str = os.getenv('DB_NAME', 'db')
    local_db_url: str = 'sqlite+aiosqlite:///issue_megener.db'
    debug: bool = bool(os.getenv('DEBUG', 'True'))

    @property
    def get_db_url(self):
        """
        Application settings loaded from environment variables.

        Attributes:
            fastapi_title (str): Title for FastAPI docs.
            fastapi_description (str): Description for FastAPI docs.
            db_dialect (str): Database dialect for SQLAlchemy.
            db_driver (str): Database driver for SQLAlchemy.
            db_user (str): Database username.
            db_password (str): Database password.
            db_host (str): Database host.
            db_port (str): Database port.
            db_name (str): Database name.
            local_db_url (str): URL for local SQLite database.
            debug (bool): Debug mode flag.
                - If True, use SQLite; otherwise, use production DB.
        """
        if self.debug:
            return self.local_db_url
        else:
            return (
                f'{self.db_dialect}+{self.db_driver}://'
                f'{self.db_user}:{self.db_password}@'
                f'{self.db_host}:{self.db_port}/'
                f'{self.db_name}'
            )


settings = Settings()
