from aiogram.utils.markdown import hbold

choose_pay_type_text = '👇 Выберите тип оплаты'

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

balance_pay_successfully_text = '☺️ Платеж прошел успешно\n' \
                                '💰 Текущий баланс: <b>{balance}</b> RUB.'

new_balance_pay_successfully_text = '\n'.join([
    '☺️ Платеж прошел успешно',
    '💰 Текущий баланс: <b>{balance}</b> RUB.'
])

pay_yoomoney_text = "💸 Оплата по <a href='{base_url}'>ссылке</a>\n" \
                    "<b>Оплачивать необходимо через форму по ссылке, " \
                    "иначе оплата не будет засчитана!</b>"

pay_qiwi_text = "💸 Можно оплатить по номеру телефона или по <a href='{base_url}'>ссылке</a>\n" \
                "Обязательно укажите id платежа: <b>{id}</b>!"

balance_up_text = f'💰 Текущий баланс: {hbold("{balance}")} RUB\n\n' \
                  'Введите сумму в рублях для пополнения баланса (целым числом)\n' \
                  f'Пример: {hbold("10")}'

pay_crypto_bot_text = "💸 Оплатите счет по <a href='{base_url}'>ссылке</a>"
