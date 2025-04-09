import os
from typing import Optional, Type, Tuple

from pydantic import Field, BaseModel, SecretStr
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
    YamlConfigSettingsSource,
    PydanticBaseSettingsSource
)


API_STATIC_PATH = '/static'
ENV_FILE = os.getenv('GYM_API__CONFIG__ENV_FILE')
CONFIG_FILE_PATH = os.getenv('GYM_API__CONFIG')


class Redis(BaseModel):
    host: Optional[str] = Field(
        None,
        description='Хост'
    )
    port: Optional[int] = Field(
        None,
        description='Порт'
    )
    password: Optional[str] = Field(
        None,
        description='Пароль'
    )


class Database(BaseModel):
    database: Optional[str] = Field(
        description='Название БД'
    )
    host: Optional[str] = Field(
        description='Хост'
    )
    login: Optional[str] = Field(
        description='Логин'
    )
    port: Optional[int] = Field(
        description='Порт'
    )
    password: Optional[SecretStr] = Field(
        description='Пароль'
    )
    drivername: str = Field(
        'postgresql+asyncpg',
        description='Название драйвера'
    )   

class GymSettings(BaseModel):
    db: Database = Field(
        default_factory=Database,
        description='Настройка postgres'
    )
    redis: Redis = Field(
        default_factory=Redis,
        description='Настройки redis'
    )

class Settings(BaseSettings):
    gym_api: GymSettings = Field(
        default_factory=GymSettings,
        description='Настройки библиотеки'
    )

    model_config = SettingsConfigDict(
        env_nested_delimiter='__',
        env_file=ENV_FILE,
        env_file_encoding='utf-8',
        extra='ignore'  # или 'forbid' для строгой проверки
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (
            dotenv_settings,
            env_settings,
            init_settings,
            YamlConfigSettingsSource(
                settings_cls=settings_cls,
                yaml_file=CONFIG_FILE_PATH
            ),
            file_secret_settings
        )

config: GymSettings = Settings().gym_api
db = config.db
redis = config.redis
print(Settings())
