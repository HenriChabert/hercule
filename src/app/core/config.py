import os
from enum import Enum

from pydantic_settings import BaseSettings, SettingsConfigDict
from starlette.config import Config


current_file_dir = os.path.dirname(os.path.realpath(__file__))

env_filename = ".env"
if os.environ.get("ENVIRONMENT") == "test":
  env_filename = ".env.test"

env_path = os.path.join(current_file_dir, "..", "..", "..", env_filename)
config = Config(env_path)

class ConfigSettings(BaseSettings):
  CONFIG_DIR: str = config("CONFIG_DIR", default=current_file_dir)
  ABSOLUTE_CONFIG_DIR: str = os.path.expanduser(os.path.expanduser(config("CONFIG_DIR", default=current_file_dir)))

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
  HERCULE_SECRET_KEY: str = config("HERCULE_SECRET_KEY", default="my_secret_key")
  HERCULE_HEADER_NAME: str = config("HERCULE_HEADER_NAME", default="X-Hercule-Secret-Key")

class DatabaseSettings(BaseSettings):
  pass

class TestSettings(BaseSettings):
  SQLITE_URI_TEST: str = config("SQLITE_URI_TEST", default="./sql_app_test.db")

class SQLiteSettings(BaseSettings):
  SQLITE_DB_NAME: str = config("SQLITE_DB_NAME", default="sql_app.db")
  SQLITE_SYNC_PREFIX: str = config("SQLITE_SYNC_PREFIX", default="sqlite:///")
  SQLITE_ASYNC_PREFIX: str = config("SQLITE_ASYNC_PREFIX", default="sqlite+aiosqlite:///")

  @property
  def SQLITE_URI(self) -> str:
    config_settings = ConfigSettings()
    return f"{config_settings.ABSOLUTE_CONFIG_DIR}/{self.SQLITE_DB_NAME}"


class EnvironmentOption(Enum):
  TEST = "test"
  DEV = "dev"
  LOCAL = "local"
  STAGING = "staging"
  PRODUCTION = "production"


class EnvironmentSettings(BaseSettings):
  ENVIRONMENT: EnvironmentOption = config("ENVIRONMENT", default=EnvironmentOption.LOCAL)

class Settings(
  ConfigSettings,
  DatabaseSettings,
  AppSettings,
  SQLiteSettings,
  TestSettings,
  SecuritySettings,
  EnvironmentSettings,
  BaseSettings
):
  model_config = SettingsConfigDict(
    env_file = ".env",
    extra='ignore'
  )


settings = Settings()