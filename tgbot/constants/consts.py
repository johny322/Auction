from pathlib import Path

# bot settings
MAX_ABOUT_LENGTH = 300
MAX_PROFILE_PHOTO_COUNT = 5
MIN_DAYS_COUNT_FOR_CHANGE_PROFILE_DATA = 30
TERMS_OF_USE_URL = 'https://telegra.ph/Polzovatelskoe-soglashenie-11-21-6'
TERMS_OF_USE_FILE_NAME = 'Пользовательское соглашение.pdf'

TEMPLATE_DATE_FORMAT = '%d.%m.%Y'
THROTTLE_TIME = 0.4  # период троттлинга в секундах
BLOCKED_THROTTLE_TIME = 10

SHOW_PHONE_NUMBER_COST = 100

REDIS_MEDIA_GROUP_TEMPLATE = '{user_id}_media_group_ids'

MAIN_PHOTO_LOGO_URL = 'https://telegra.ph//file/0191977e9befc6365424d.jpg'
PAYMENT_PHOTO_URL = ''

BLUR_LOGO_FILE_NAME = ''

MEDIA_DIR = 'media'
MEDIA_DIR_PATH = Path(__file__).resolve().parent.parent / MEDIA_DIR

MAIN_LOGO_FILE = 'main_logo.jpeg'
MAIN_LOGO_FILE_PATH = MEDIA_DIR_PATH / MAIN_LOGO_FILE

TERMS_OF_USE_FILE_PATH = MEDIA_DIR_PATH / TERMS_OF_USE_FILE_NAME

DAYS_STR = ('день', 'дня', 'дней')
