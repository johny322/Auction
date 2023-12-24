import datetime

import pytz


def get_now_datetime() -> datetime.datetime:
    return datetime.datetime.now(pytz.timezone("Europe/Moscow")).replace(tzinfo=None)


def get_now_date() -> datetime.datetime.date:
    return datetime.datetime.now(pytz.timezone("Europe/Moscow")).replace(tzinfo=None).date()


if __name__ == '__main__':
    print(get_now_datetime().date())
