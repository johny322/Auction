import datetime
from copy import deepcopy
from dataclasses import dataclass

from tgbot.misc.utils.text import escape


@dataclass
class UserTypeStr:
    girl = 'girl'
    boy = 'boy'


@dataclass
class UserStatusStr:
    not_registered = 'not_registered'
    under_review = 'under_review'
    normal = 'normal'
    common = 'common'
    gold = 'gold'
    diamond = 'diamond'


@dataclass
class RegisterData:
    name: str = None
    full_name: str = None
    country: str = None
    city_full_name: str = None
    birthday: datetime.datetime.date = None
    about: str = None
    breast_size: float = None
    height: int = None
    weight: int = None
    mobile_phone: str = None
    wa: bool = None
    tg: str = None
    user_type: str = None

    def get_kwargs(self):
        data = deepcopy(self.__dict__)
        data.pop('user_type', None)

        return data

    def escape_all(self):
        return RegisterData(
            name=escape(self.name),
            full_name=escape(self.full_name),
            country=escape(self.country),
            city_full_name=escape(self.city_full_name),
            birthday=self.birthday,
            about=escape(self.about),
            breast_size=self.breast_size,
            height=self.height,
            weight=self.weight,
            wa=self.wa,
            mobile_phone=escape(self.mobile_phone),
            tg=escape(self.tg),
        )


@dataclass
class UserFileTypeStr:
    photo = 'photo'
    video = 'video'


@dataclass
class MenuPart:
    review_reg_data = 'rrd'
    search_girls_city = 'search_girls_city'
    search_pagination = 'sp'


@dataclass
class SubTypeStr:
    boy = 'boy'
    girl = 'girl'


@dataclass
class PaymentTypeStr:
    telegram = 'telegram'
    anypay = 'anypay'


@dataclass
class Country:
    Russia = 'Russia'

    @property
    def names(self):
        return [self.Russia]


@dataclass
class LanguageStr:
    ru = 'ru'
