from pathlib import Path

# bot settings
ADMIN_PERCENT = 12
ONLY_ONE_BET_WINNER_PERCENT = 110
ANYPAY_MIN_PAYMENT_SIZE = 100
MINIMAL_BET_SIZE = 10  # минимальная ставка для начала аукциона в руб
# AUCTION_FIRST_TIME_LIMIT = 60  # 12 * 60 * 60  # 12 часов
# AUCTION_ROUND_TIME_LIMIT = 10  # 8 * 60  # 8 минут
AUCTION_FIRST_TIME_LIMIT = 12 * 60 * 60  # 12 часов
AUCTION_ROUND_TIME_LIMIT = 8 * 60  # 8 минут

PAYOUT_MIN_SUM_FOR_ALERT = 1000
CRYPTO_BOT_PAYOUT_MIN_SIZE = 200
ANYPAY_BOT_PAYOUT_MIN_SIZE = 500

TEMPLATE_DATE_FORMAT = '%d.%m.%Y, %H:%M:%S'
THROTTLE_TIME = 0.4  # период троттлинга в секундах
BLOCKED_THROTTLE_TIME = 10

REDIS_MEDIA_GROUP_TEMPLATE = '{user_id}_media_group_ids'

MAIN_PHOTO_LOGO_URL = ''

MEDIA_DIR = 'media'
MEDIA_DIR_PATH = Path(__file__).resolve().parent.parent / MEDIA_DIR

MAIN_LOGO_FILE = 'main_logo.jpeg'
MAIN_LOGO_FILE_PATH = MEDIA_DIR_PATH / MAIN_LOGO_FILE

DAYS_STR = ('день', 'дня', 'дней')
