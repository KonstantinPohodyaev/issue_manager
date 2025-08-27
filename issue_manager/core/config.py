import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    fastapi_title: str = os.getenv('FASTAPI_TITLE', 'Issue_manager')
    fastapi_description: str = os.getenv('FASTAPI_DESCRIPTION', '')
    db_dialect: str = os.getenv('DB_DIALECT', 'postgresql')
    db_driver: str = os.getenv('DB_DRIVER', 'asyncpg')
    db_user: str = os.getenv('DB_USER', 'user')
    db_password: str = os.getenv('DB_PASSWORD', 'password')
    db_host: str = os.getenv('DB_HOST', 'db')
    db_port: str = os.getenv('DB_PORT', '5432')
    db_name: str = os.getenv('DB_NAME', 'db')
    test_db_url: str = 'sqlite+aiosqlite:///test_db.db'
    debug: bool = bool(os.getenv('DEBUG', 'True'))

    @property
    def get_db_url(self):
        return (
            f'{self.db_dialect} + {self.db_driver}://'
            f'{self.db_user}:{self.db_password}@'
            f'{self.db_host}:{self.db_port}/'
            f'{self.db_name}'
        )


settings = Settings()
