import logging

from pyrogram import Client
from yoomoney import Client as YClient

from tgbot.config import load_config
from tgbot.services.payments.banker import Banker


def setup_logger():
    logger = logging.getLogger('main_logger')
    logger.propagate = False
    logger.setLevel(logging.DEBUG)
    # strfmt = '[%(asctime)s] [%(levelname)s] %(message)s'
    strfmt = "[%(asctime)s] [%(levelname)-8s] --- %(message)s (%(filename)s:%(funcName)s:%(lineno)s)"

    datefmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(strfmt, datefmt)

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.info('Set up logger')
    # logger.info('Set up logger', extra={'d': {'detail': 'new line'}})

    return logger


logger = setup_logger()

config = load_config(".env")

client = Client('banker', config.misc.telegram_api_id, config.misc.telegram_api_hash)
yclient = YClient(config.payments.yoomoney_token)
banker = Banker(client)
