mailing_post_text = """
👋 <b>Отправьте мне сообщение для рассылки, бот принимает фото, видео и просто текст</b>
"""

mail_sure_text = "<b>Отправить это?</b>"

mail_statistic_text = """
<b>Начинаю рассылку!</b>

Отправлено: <b>{msg_count}</b>
Заблокировали бота: <b>{block_count}</b> 
Другая ошибка: <b>{error_count}</b>

Последнее обновление
<b>{last_update}</b>
"""

mail_end_text = "<b>Рассылка закончилась</b>"
mail_cancel_text = "<b>Рассылка отменена</b>"

users_count_text = 'Число пользователей в боте: <b>{users_count}</b>'

no_users_balance_text = 'Не найдено юзеров с балансом больше {balance}'
users_balance_text = '✔  {full_name} (@{username}) баланс: {balance}'

no_find_user_args_text = 'Необходимо вместе с командой отправить tg id или username пользователя'
no_find_user_text = 'Пользователя с tg id или username {args} не найдено'

add_user_balance_sum_text = 'Пользователь: @{username} {fullname} {user_id}\n' \
                            'Введите сумму для пополнения баланса'

bad_format_balance_sum_text = 'Неверный формат баланса'

confirming_add_user_balance_text = 'Пополнить баланс для пользователя:\n' \
                                   '@{username} {full_name} {user_id}\n' \
                                   'с текущим балансом: {current_balance}\n' \
                                   'на сумму {balance_sum} RUB?'

good_add_user_balance_text = 'Баланс успешно пополнен'

confirming_user_disable_advertising_text = 'Отключить рекламу для пользователя:\n' \
                                           '@{username} {fullname} {user_id}?'

good_disable_advertising_text = 'Реклама у пользователя успешно отключена'

confirm_user_reg_data_text = 'Подтвердить данные нового пользователя (tg id: {tg_user_id})?\n' \
                             'Последняя фотография не будет отображаться в карточке и нужна только для ' \
                             'подтверждения личности'

confirm_change_account_data_text = 'Подтвердить <b>новые</b> данные старого пользователя (tg id: {tg_user_id})?\n' \
                                   'Последняя фотография не будет отображаться в карточке и нужна только для ' \
                                   'подтверждения личности'

good_confirm_user_reg_data_text = 'Данные подтверждены'
answer_review_text = 'Отправьте причину отказа подтверждения'
confirm_answer_review_text = 'Отправить данное сообщение?\n{}'
good_answer_review_text = 'Сообщение было отправлено'
