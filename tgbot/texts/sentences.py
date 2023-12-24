import datetime

from dateutil import relativedelta

from tgbot.constants.consts import TEMPLATE_DATE_FORMAT
from tgbot.constants._types import RegisterData, UserTypeStr, UserStatusStr
from tgbot.db.models import User, UserStatus, UserType
from tgbot.misc.utils.date_worker import get_now_datetime

start_user_message_text = '👋 Добро пожаловать!'
first_start_user_message_text = '👋 Добро пожаловать!\n' \
                                'Для использования бота необходимо пройти регистрацию\n' \
                                '👇 Выберите нужный пункт'

agree_agreement_message_text = 'Для использования бота вам необходимо подтвердить пользовательское соглашение'
good_agree_agreement_message_text = 'Отлично. Теперь вы можете пользоваться ботом'
already_agree_agreement_message_text = 'Вы уже подтвердили соглашение'

start_admin_message_text = '👋 Добро пожаловать, админ!\n' \
                           '/admin - просмотр команд админа'

new_referral_info_text = '👥 Вы стали рефералом <b>{full_name}</b>'

choose_menu_text = '👇 Выберите нужный пункт'

success_cancel_text = '❎ Ваше действие отменено'

admin_info_message_text = "👤 Администратор бота: @{admin}"

disable_advertising_info_text = '❇️ По поводу отключения рекламы писать администратору бота\n' \
                                '👤 Администратор бота: @{admin}'

referral_system_info_text = '👥 Ваша реферальная ссылка: {link}\n\n' \
                            '👥 Число ваших рефералов: <b>{ref_count}</b>\n' \
                            '💸 Вы будете получать {percents}% на свой счёт за каждое пополнение вашим рефералом'

terms_of_use_text = 'Пользовательское соглашение <a href="{}">тут</a>'
terms_of_use_caption_text = 'Пользовательское соглашение'

anti_flood_message_text = 'Не спамь! Перерыв {}с'

####################################
empty_text = '⠀'

previous_answer_text = 'Вы ввели {}'

reg_full_name_text = 'Отправьте ваши имя и фамилию'
reg_name_text = 'Отправьте ваше имя для отображения в боте'
reg_country_text = 'Отправьте название страны, в которой вы проживаете'
reg_city_text = 'Отправьте название города, в котором вы проживаете\n' \
                'Воспользуйтесь кнопкой поиск ниже'
bad_city_text = 'Выберите город из списка. ' \
                'Для поиска следует написать начало названия города и бот сам предложит варианты'
reg_about_text = 'Отправьте короткую информация о себе (не более {} символов) без указания контактов'
so_long_about_text = 'Слишком длинная информация. Пожалуйста сократите текст до {} символов'
reg_birthday_text = 'Отправьте вашу дату рождения в формате dd.mm.yyyy'
bad_format_reg_birthday_text = 'Неверный формат даты'

reg_breast_size_text = 'Отправьте ваш размер груди числом'
reg_height_text = 'Отправьте ваш рост в сантиметрах числом'
reg_weight_text = 'Отправьте ваш вес в кг числом'

bad_digit_format_text = 'Неверный формат. Отправьте число'

reg_mobile_phone_text = 'Отправьте полный номер телефона с кодом страны'
bad_format_reg_mobile_phone_text = 'Неверный формат номера телефона'

reg_wa_text = 'Есть ли данный номер в whatsapp?'
reg_tg_text = 'Отправьте ваш ник в телеграмме в формате @username'
bad_format_reg_tg_text = 'Неверный формат ника в телеграмме'

use_keyboard_for_answer_text = 'Пожалуйста используйте кнопки ниже для ответа'

# girls register
photo_reg_text = 'Отправьте ваши фотографии и видео (не более {}) для отображения в боте\n' \
                 'После отправки файлов нажмите на кнопку подтвердить.\n' \
                 'Фото и видео необходимо отправлять с сжатием, а не файлом'
photo_already_added_text = 'Данная фотография уже добавлена'
max_photo_added_text = 'Добавлено максимальное количество файлов({})'

send_reg_template_text = "Пожалуйста напишите свои данные по следующему шаблону и отправьте сообщением боту:\n" \
                         "# Name: ваше имя, которое будет отображаться в боте\n" \
                         "# Full name: ваши фамилия и имя\n" \
                         "# Country: страна, в которой вы проживаете\n" \
                         "# City: город, в котором вы проживаете\n" \
                         "# Birthday: дата рождения в формате dd.mm.yyyy\n" \
                         "# About: коротка информация о себе (не более 300 символов) без указания контактов\n" \
                         "# Mobile phone: полный номер телефона с кодом страны\n" \
                         "# wa: есть ли данный номер в whatsapp; поставить символ '+' если есть, символ '-' если нет\n" \
                         "# tg: ник в телеграмме в формате @username, если есть, иначе поставить - или пропустить поле"

pre_example_reg_text = 'Пример заполнения шаблона'
example_reg_text = "# Name: Анастасия\n" \
                   "# Full name: Иванова Анастасия\n" \
                   "# Country: Россия\n" \
                   "# City: Москва\n" \
                   "# Birthday: 20.10.2000\n" \
                   "# About: люблю заниматься спортом, читать и проводить классно время 😘\n" \
                   "будем проводить время вместе🤗\n" \
                   "# Mobile phone: +79991234567\n" \
                   "# wa: +\n" \
                   "# tg: @tg_user_name"

confirm_main_reg_data_text = 'Все данные введены верно?'
confirm_photo_reg_data_text = 'Фото и видео верны?'
confirm_check_photo_data_text = 'Фото верно?'

send_photo_to_admin_text = 'Отправьте селфи с документом, подтверждающим вашу личность. ' \
                           'Это необходимо для проверки веденных вами данных'

user_reg_card_text = 'Ваша карточка в боте будет выглядеть так'
check_photo_data_text = 'Данная фотография отправится администратору на проверку личности'

good_confirm_reg_data_text = 'Ваша информация отправлена на проверку. Как только мы проверим ваши данные, ' \
                             'вы получите информацию об этом. В случаи неверный данных, вы сможете пройти регистрацию ' \
                             'повторно и исправить неверные данные.\n' \
                             'После успешной проверки вы сможете полноценно ' \
                             'пользоваться данным ботом'

good_confirm_change_account_data_text = 'Ваша информация отправлена на проверку. Как только мы проверим ваши данные, ' \
                                        'вы получите информацию об этом. В случаи неверный данных, вы сможете обновить информацию ' \
                                        'повторно и исправить неверные данные.\n' \
                                        'После успешной проверки ваша информация профиля обновится'

good_review_reg_data_text = 'Проверка была пройдена успешно, теперь вы можете использовать полный функционал бота'
good_review_change_account_data_text = 'Проверка была пройдена успешно, информация вашего профиля обновлена'
bad_review_reg_data_text = 'Проверка была пройдена неудачно\n' \
                           'Сообщение от администратора:\n{}'

search_girls_city_text = 'Выберите город, в котором хотите найти девушку\n' \
                         'Для этого нажмите на кнопку поиска и в списке выберите нужный город.\n' \
                         'Для более простого поиска воспользуйтесь клавиатурой и введите название города'

bad_search_girls_city_text = 'Пожалуйста, выберите город из списка'

need_sub_for_info_text = 'Для получения полной информации приобретите подписку'

search_end_text = 'Девушки в данном городе закончились'

choose_sub_type_text = 'Выберите период подписки'

account_statistics_text = 'Число просмотров карточки за сегодня: {day_views_count}\n' \
                          'Число просмотров номера телефона за сегодня: {day_phone_views_count}'

day_limit_change_account_data_text = 'Вы можете менять данные аккаунта не чаще одного раза в {day_int} {day_str} ' \
                                     '(т.е. каждые {day_int} {day_str})'


async def get_profile_text(user: User, user_status: UserStatus, user_type: UserType) -> str:
    if user_type.name == UserTypeStr.boy:
        user_type_text = 'мужчина 👱‍♂️'
    else:
        user_type_text = 'девушка 👱‍♀️'
    status_text = get_status_text(user_status.name)

    subscription_expiration = user.subscription_expiration
    if get_now_datetime() > subscription_expiration:
        subscription_expiration_text = 'отсутствует'
    else:
        subscription_expiration_text = 'действует до {}'.format(
            subscription_expiration.strftime(TEMPLATE_DATE_FORMAT)
        )
    text = f'Тип аккаунта: {user_type_text}\n' \
           f'Статус аккаунта: {status_text}\n' \
           f'Подписка: {subscription_expiration_text}'
    return text


def get_status_text(status: str) -> str:
    if status == UserStatusStr.gold:
        status_text = 'золотой 🟡'
    elif status == UserStatusStr.diamond:
        status_text = 'брилиантовый 💎'
    else:
        status_text = 'обычный 🟢'
    return status_text


def fill_template(data: RegisterData, blur=False, hide_mobile_phone=True) -> str:
    data = data.escape_all()
    wa = 'есть' if data.wa else 'нет'
    if data.tg:
        tg = '@' + data.tg if not data.tg.startswith('@') else data.tg
    else:
        tg = 'нет'
    years = relativedelta.relativedelta(datetime.datetime.now().date(), data.birthday).years
    if blur:
        mobile_phone = f'<tg-spoiler>номер скрыт для вас</tg-spoiler>'
        tg = f'<tg-spoiler>telegram скрыт для вас</tg-spoiler>'
        extra_info = '\n\n' \
                     f'<b>{need_sub_for_info_text}</b>'
    else:
        mobile_phone = f'<code>{data.mobile_phone}</code>'
        extra_info = ''
    rows = [
        f"Имя: {data.name}",
        f"Полное имя: {data.full_name}",
        f"Страна: {data.country}",
        f"Город: {data.city_full_name}",
        f"Возраст: {years}",
        f"О себе: {data.about}",
        f"Размер груди: {data.breast_size}",
        f"Рост: {data.height} см",
        f"Вес: {data.weight} кг",
    ]
    if not hide_mobile_phone:
        rows.append(
            f"Номер телефона: {mobile_phone}",
        )
    rows.extend(
        [
            f"Whatsapp: {wa}",
            f"Telegram: {tg}" + extra_info
        ]
    )
    text = '\n'.join(rows)
    return text
