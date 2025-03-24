import os
from typing import Literal, TypeAlias, cast

from pydantic_settings import BaseSettings, SettingsConfigDict
from starlette.config import Config

current_file_dir = os.path.dirname(os.path.realpath(__file__))
project_src_dir = os.path.dirname(os.path.dirname(current_file_dir))
project_root_dir = os.path.dirname(project_src_dir)

secrets_dir = os.path.join(project_root_dir, "secrets")

env_filename = ".env"
if os.environ.get("ENVIRONMENT") == "test":
    env_filename = ".env.test"

print(os.environ.get("ENVIRONMENT"))
env_path = os.path.join(project_root_dir, env_filename)
config = Config(env_path)


class ConfigSettings(BaseSettings):
    CONFIG_DIR: str = config("CONFIG_DIR", default=current_file_dir)
    ABSOLUTE_CONFIG_DIR: str = os.path.expanduser(
        os.path.expanduser(config("CONFIG_DIR", default=current_file_dir))
    )


config_settings = ConfigSettings()


class LoggingSettings(BaseSettings):
    @property
    def LOG_DIR(self) -> str:
        return f"{config_settings.ABSOLUTE_CONFIG_DIR}/logs"


class AppSettings(BaseSettings):
    APP_NAME: str = config("APP_NAME", default="FastAPI app")
    APP_DESCRIPTION: str = config("APP_DESCRIPTION", default="")
    APP_VERSION: str = config("APP_VERSION", default="0.0.1")
    LICENSE_NAME: str | None = config("LICENSE", default=None)
    CONTACT_NAME: str | None = config("CONTACT_NAME", default=None)
    CONTACT_EMAIL: str | None = config("CONTACT_EMAIL", default=None)
    SECRET_KEY: str = config("JWT_SECRET_KEY", default="your-secret-key-here")


class SecuritySettings(BaseSettings):
    HERCULE_PORT: int = config("HERCULE_PORT", default=8000)
    HERCULE_PWD: str = config("HERCULE_PWD", default="")


class AuthSettings(BaseSettings):
    AUTH_REQUIRED: bool = config("AUTH_REQUIRED", default=True)


class DatabaseSettings(BaseSettings):
    pass


class SQLiteSettings(BaseSettings):
    SQLITE_DB_NAME: str = config("SQLITE_DB_NAME", default="sql_app.db")
    SQLITE_SYNC_PREFIX: str = config("SQLITE_SYNC_PREFIX", default="sqlite:///")
    SQLITE_ASYNC_PREFIX: str = config(
        "SQLITE_ASYNC_PREFIX", default="sqlite+aiosqlite:///"
    )

    @property
    def SQLITE_DB_PATH(self) -> str:
        return f"{config_settings.ABSOLUTE_CONFIG_DIR}/{self.SQLITE_DB_NAME}"

    @property
    def SQLITE_URI(self) -> str:
        return f"{self.SQLITE_ASYNC_PREFIX}{self.SQLITE_DB_PATH}"


EnvironmentOption: TypeAlias = Literal["test", "dev", "local", "staging", "production"]


class EnvironmentSettings(BaseSettings):
    ENVIRONMENT: EnvironmentOption = cast(
        EnvironmentOption, config("ENVIRONMENT", default="local")
    )


class WebPushSettings(BaseSettings):
    APP_SERVER_KEY: str = config("APP_SERVER_KEY", default="")
    SUBSCRIBER_EMAIL: str = config("SUBSCRIBER_EMAIL", default="chabhenrib@gmail.com")
    PUBLIC_KEY_PATH: str = config(
        "PUBLIC_KEY_PATH", default=os.path.join(secrets_dir, "public_key.pem")
    )
    PRIVATE_KEY_PATH: str = config(
        "PRIVATE_KEY_PATH", default=os.path.join(secrets_dir, "private_key.pem")
    )


class ApiSettings(BaseSettings):
    API_URL: str = config("API_URL", default="http://localhost:8000/api/v1")


class Settings(
    ConfigSettings,
    DatabaseSettings,
    AppSettings,
    SQLiteSettings,
    SecuritySettings,
    EnvironmentSettings,
    WebPushSettings,
    ApiSettings,
    AuthSettings,
    LoggingSettings,
    BaseSettings,
):
    model_config = SettingsConfigDict(env_file=env_filename, extra="ignore")


settings = Settings()
