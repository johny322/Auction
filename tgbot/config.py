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
class Miscellaneous:
    yoomoney_token: str
    yoomoney_receiver: int
    telegram_api_id: str
    telegram_api_hash: str


@dataclass
class ApiKeys:
    sms_activate: str
    onlinesim: str
    sms_acktiwator: str
    vak_sms: str
    sms_365: str


@dataclass
class Payments:
    yoomoney_token: str
    yoomoney_receiver: int
    qiwi_token: str
    qiwi_number: str
    qiwi_pubkey: str
    crypto_bot_token: str


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    misc: Miscellaneous
    api_keys: ApiKeys
    payments: Payments


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
        misc=Miscellaneous(
            yoomoney_token=env.str('YOOMONEY_TOKEN'),
            yoomoney_receiver=env.int('YOOMONEY_RECEIVER'),
            telegram_api_id=env.str('TELEGRAM_API_ID'),
            telegram_api_hash=env.str('TELEGRAM_API_HASH'),
        ),
        api_keys=ApiKeys(
            sms_activate=env.str('SMS_ACTIVATE_KEY'),
            onlinesim=env.str('ONLINESIM_KEY'),
            sms_acktiwator=env.str('SMS_ACKTIWATOR'),
            vak_sms=env.str('VAK_SMS'),
            sms_365=env.str('SMS_365'),
        ),
        payments=Payments(
            yoomoney_token=env.str('YOOMONEY_TOKEN'),
            yoomoney_receiver=env.int('YOOMONEY_RECEIVER'),
            qiwi_token=env.str('QIWI_TOKEN'),
            qiwi_number=env.str('QIWI_NUMBER'),
            qiwi_pubkey=env.str('QIWI_PUBKEY'),
            crypto_bot_token=env.str('CRYPTO_BOT_TOKEN'),
        )
    )
