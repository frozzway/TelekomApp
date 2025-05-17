from pathlib import Path
from zoneinfo import ZoneInfo

from alembic.config import Config
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    server_host: str = '0.0.0.0'
    server_port: int = '5007'
    timezone: str = 'Asia/Yekaterinburg'
    server_environment: str = ''

    db_username: str = 'postgres'
    db_password: str = '123'
    db_host: str = '127.0.0.1'
    db_port: str = '5432'
    db_database: str = 'TelekomTest'
    db_dialect: str = 'mysql+pymysql'
    db_migrations_path: str = str(Path.cwd() / 'alembic_migrations')

    jwt_expires_s: int = 60 * 30
    jwt_refresh_token_expires_s: int = 60 * 60 * 24 * 7
    jwt_cookie_name: str = 'TelekomTestCookie'
    jwt_secret: str = 'a99ef8a3a0734e2d820dc323a29b787235ab7ec504a870ca0ff8c9df5f058042'
    jwt_algorithm: str = 'HS256'
    bcrypt_salt: bytes = b'$2b$12$zLOG0G7NjDvxAgnae7srnu'


settings = Settings()

alembic_config_path = Path(settings.db_migrations_path) / "alembic.ini"
alembic_scripts_path = Path(settings.db_migrations_path) / "script"

alembic_cfg = Config(alembic_config_path)
alembic_cfg.set_main_option("script_location", str(alembic_scripts_path))

timezone = ZoneInfo(settings.timezone)
