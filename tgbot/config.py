from dataclasses import dataclass
from typing import List

from environs import Env
from sqlalchemy.engine.url import URL


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str
    drivername: str
    port: int = None

    def create_url(self) -> URL:
        url = URL.create(
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port or 5432,  # postgresql default port
            database=self.database,
            drivername=self.drivername  # 'postgresql+asyncpg'
        )
        return url


@dataclass
class DbRedis:
    host: str
    port: str
    db: str
    username: str = None
    password: str = None

    def get_kwargs(self):
        return self.__dict__


@dataclass
class TgBot:
    token: str
    bot_username: str
    admin_ids: List[int]
    use_redis: bool
    admin_username: str
    provider_token: str

    def bot_link(self):
        return f'https://t.me/{self.bot_username}'


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    db_redis: DbRedis


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            bot_username=env.str("BOT_USERNAME"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            use_redis=env.bool("USE_REDIS"),
            admin_username=env.str('ADMIN_USERNAME'),
            provider_token=env.str('PROVIDER_TOKEN'),

        ),
        db=DbConfig(
            host=env.str('DB_HOST'),
            port=env.int('DB_PORT'),
            password=env.str('DB_PASS'),
            user=env.str('DB_USER'),
            database=env.str('DB_NAME'),
            drivername=env.str('DB_DRIVERNAME'),
        ),
        db_redis=DbRedis(
            host=env.str('DB_REDIS_HOST'),
            port=env.str('DB_REDIS_PORT'),
            db=env.int('DB_REDIS_NAME'),
            username=env.str('DB_REDIS_USER', None),
            password=env.str('DB_REDIS_PASSWORD', None),

        )
    )
