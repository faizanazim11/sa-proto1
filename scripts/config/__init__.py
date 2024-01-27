import os
import pathlib
from typing import Optional

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings

PROJECT_NAME = "skillarena_proto1"


class _Services(BaseSettings):
    # Microservice Specifics
    PORT: int = Field(default=3001, validation_alias="service_port")
    HOST: str = Field(default="0.0.0.0", validation_alias="service_host")
    ENABLE_SSL: bool = Field(default=True, validation_alias="enable_ssl")

    # Logging
    LOG_LEVEL: str = "INFO"
    ENABLE_FILE_LOG: Optional[bool] = False
    ENABLE_CONSOLE_LOG: Optional[bool] = True
    LOG_ENABLE_TRACEBACK: bool = Field(default=False)

    @model_validator(mode="before")
    def validate_log_level_and_hosts(cls, values):
        values["LOG_LEVEL"] = values.get("LOG_LEVEL", "INFO")
        print(f"Logging Level set to : {values['LOG_LEVEL']}")
        return values


class _SecurityConstants(BaseSettings):
    LOCK_OUT_TIME_IN_MINS: int = 30
    ALGORITHM: str = "HS256"
    ISSUER: str = "skillarena"
    TOKEN: str = "b8133b13-b0a0-49b5-a632-ac0ded436f11"


class _PathToStorage(BaseSettings):
    BASE_PATH: pathlib.Path = Field(None, validation_alias="BASE_PATH")
    MOUNT_DIR: pathlib.Path = Field(None, validation_alias="MOUNT_DIR")
    MODULE_PATH: Optional[pathlib.Path]
    LOGS_MODULE_PATH: Optional[pathlib.Path]

    @model_validator(mode="before")
    def path_merger(cls, values):
        values["LOGS_MODULE_PATH"] = os.path.join(values.get("BASE_PATH"), "logs", values.get("MOUNT_DIR"))
        values["MODULE_PATH"] = os.path.join(values.get("BASE_PATH"), values.get("MOUNT_DIR"))
        return values


class _Databases(BaseSettings):
    MONGO_URI: str
    POSTGRES_URI: str
    REDIS_URI: str


class _AIConfig(BaseSettings):
    PROJECT: str
    REGION: str


Services = _Services()
SecurityConstants = _SecurityConstants()
Databases = _Databases()
PathToStorage = _PathToStorage()
AIConfig = _AIConfig()

__all__ = ["Services", "SecurityConstants", "Databases", "PathToStorage", "AIConfig"]
