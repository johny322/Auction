from dataclasses import dataclass
from typing import List

from environs import Env


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str


@dataclass
class TgBot:
    token: str
    bot_username: str
    admin_ids: List[int]
    use_redis: bool
    admin_username: str

    def bot_link(self):
        return f'https://t.me/{self.bot_username}'


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            bot_username=env.str("BOT_USERNAME"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            use_redis=env.bool("USE_REDIS"),
            admin_username=env.str('ADMIN_USERNAME')
        ),
        db=DbConfig(
            host=env.str('DB_HOST'),
            password=env.str('DB_PASS'),
            user=env.str('DB_USER'),
            database=env.str('DB_NAME')
        ),
    )
