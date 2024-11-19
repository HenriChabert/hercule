import os
from enum import Enum

from pydantic_settings import BaseSettings
from starlette.config import Config

current_file_dir = os.path.dirname(os.path.realpath(__file__))
env_path = os.path.join(current_file_dir, "..", "..", "..", ".env")
config = Config(env_path)


class AppSettings(BaseSettings):
  APP_NAME: str = config("APP_NAME", default="FastAPI app")
  APP_DESCRIPTION: str = config("APP_DESCRIPTION", default="")
  APP_VERSION: str = config("APP_VERSION", default="0.0.1")
  LICENSE_NAME: str | None = config("LICENSE", default=None)
  CONTACT_NAME: str | None = config("CONTACT_NAME", default=None)
  CONTACT_EMAIL: str | None = config("CONTACT_EMAIL", default=None)

class SecuritySettings(BaseSettings):
  HERCULE_PORT: int = config("HERCULE_PORT", default=8000)
  HERCULE_PWD: str = config("HERCULE_PWD", default="")

class DatabaseSettings(BaseSettings):
  pass

class TestSettings(BaseSettings):
  SQLITE_URI_TEST: str = config("SQLITE_URI_TEST", default="./sql_app_test.db")

class SQLiteSettings(DatabaseSettings):
  SQLITE_URI: str = config("SQLITE_URI", default="./sql_app.db")
  SQLITE_SYNC_PREFIX: str = config("SQLITE_SYNC_PREFIX", default="sqlite:///")
  SQLITE_ASYNC_PREFIX: str = config("SQLITE_ASYNC_PREFIX", default="sqlite+aiosqlite:///")


class EnvironmentOption(Enum):
    LOCAL = "local"
    STAGING = "staging"
    PRODUCTION = "production"


class EnvironmentSettings(BaseSettings):
    ENVIRONMENT: EnvironmentOption = config("ENVIRONMENT", default=EnvironmentOption.LOCAL)

class Settings(
    AppSettings,
    SQLiteSettings,
    TestSettings,
    SecuritySettings,
    EnvironmentSettings
    
):
    pass

settings = Settings()