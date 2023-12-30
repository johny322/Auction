from aiogram.utils.markdown import hbold

choose_pay_type_text = '👇 Выберите способ оплаты'
choose_payout_type_text = 'Вывод CryptoBot от 200р\n' \
                          'Вывод Банковская Карта от 500р\n\n' \
                          '👇 Выберите способ оплаты'

payment_title_text = 'Оплата подписки на {}'
payment_description_text = 'Оформление подписки на нашу платформу'
payment_label_text = 'Оплата подписки'

add_balance_sum_question_text = 'Вы хотите пополнить баланс на {pay_size} руб.?'

send_banker_cheque_text = '''
Отправьте чек на сумму {pay_size}₽

🔵 Установите курс Bittrex в банкире
🔵 Чтобы оплата прошла чек должен быть в рублях, иначе оплата не зачтется
'''

banker_cheque_invalid_text = '😧 Чек неверный'

banker_checking_cheque_text = """
⏳ Подождите, это может занять некоторое время...

Если чек не обработался в течение минуты отправьте его заново
"""

banker_checking_cheque_invalid_text = """
😧 <b>Чек, который вы отправили, недействителен!</b>
"""

cheque_too_small_text = """
🔴 Чек неверной суммы, вы должны были отправить <b>{must_amount} RUB</b>, а отправили <b>{send_amount} RUB</b>, теперь вы должны докинуть недостающие деньги, написать обращение в ТП, мы выдадим вам подписку в ручную
"""

balance_pay_successfully_text = '☺️ Платеж прошел успешно'

new_balance_pay_successfully_text = '\n'.join([
    '☺️ Платеж прошел успешно',
    '💰 Текущий баланс: <b>{balance}</b> RUB.'
])

payment_need_check_text = "                                                             ❗❗❗️\n" \
                          "<b>После оплаты обязательно нажмите кнопку проверки платежа " \
                          "и не перезапускайте бота до завершения оплаты иначе оплата НЕ БУДЕТ ЗАСЧИТАНА</b>\n" \
                          "                                                             ❗❗❗"

pay_yoomoney_text = "💸 Оплата по <a href='{base_url}'>ссылке</a>\n" \
                    "<b>Оплачивать необходимо через форму по ссылке, " \
                    "иначе оплата не будет засчитана!</b>"

pay_qiwi_text = "💸 Можно оплатить по номеру телефона или по <a href='{base_url}'>ссылке</a>\n" \
                "Обязательно укажите id платежа: <b>{id}</b>!"

balance_up_text = f'💰 Текущий баланс: {hbold("{balance}")} RUB\n\n' \
                  'Введите сумму в рублях для пополнения баланса (целым числом)\n' \
                  f'Пример: {hbold("10")}'

pay_crypto_bot_text = "💸 Оплатите счет по <a href='{base_url}'>ссылке</a>"

email_pay_text = 'Отправьте свою почту для получения информации'

pay_anypay_text = "💸 Оплата по <a href='{pay_url}'>ссылке</a>\n" \
                  "<b>Оплачивать необходимо через форму по ссылке, " \
                  "иначе оплата не будет засчитана!</b>" + '\n\n' + payment_need_check_text

anypay_create_pay_error_text = '😧 При выставлении счета произошла ошибка'
minimal_pay_size_text = 'Минимальная сумма пополнения этим методом - {pay_size} RUB'
request_for_payout_text = 'Запрос на вывод {} руб отправлен'
no_balance_payout_message_text = 'У вас недостаточно баланса для вывода'
min_balance_warning_text = 'Сумма слишком маленькая\n' \
                           'Вывод от {} руб'
admin_payout_message_text = 'Запрос на вывод {payout_size} руб\n' \
                            'Пользователь: {full_name} | @{username}\n' \
                            'Метод вывода: {payment_type}\n' \
                            'Реквизиты: {payout_requisites}\n' \
                            'Текущий баланс: {balance} руб'
no_user_balance_payout_message_text = 'У пользователя недостаточно баланса для вывода'
good_payout_message_text = 'Выплата в размере {} руб успешно совершена'
bad_payout_message_text = 'Выплата отменена'
good_payout_chanel_message_text = '<b>Выплата</b>\n\n' \
                                  'Пользователь: {full_name} | @{username}\n' \
                                  'Сумма: {payout_sum} руб\n' \
                                  'Статус: {status}'
card_payout_requisites_message_text = 'Введите номер карты для зачисления'
crypto_bot_payout_requisites_message_text = 'Введите ссылку на пополнение кошелька crypto_bot'
confirm_payout_message_text = 'Проверьте правильность введенных данных:\n' \
                              'Сумма: {payout_size}\n' \
                              'Куда: {payment_type}\n' \
                              'Реквизиты: {payout_requisites}'
