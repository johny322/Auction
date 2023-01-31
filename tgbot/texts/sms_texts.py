from aiogram.utils.markdown import hcode, hbold

start_default_country_and_operator_text = '🚩 Ваша страна по умолчанию: {default_country_name}\n' \
                                          '🌐 Ваш оператор по умолчанию: {default_operator_name}\n\n' \
                                          '👇 Для их изменения выберите значения ниже'

default_country_and_operator_text = '🚩 Ваша страна по умолчанию: {default_country_name}\n' \
                                    '🌐 Ваш оператор по умолчанию: {default_operator_name}'

success_clear_favourites_list_text = '🗑 Список избранного очищен'

favorite_menu_text = '⭐ Меню избранного'
choose_find_number_menu_text = '👇 Выберите пункт для поиска избранного номера'

buy_number_text = '📱 Покупка номера'

end_find_text = '✔️ Поиск завершен'
ending_find_number_text = '⏳ Завершение поиска...'
unsuccessful_find_number_text = '😥 Не удалось найти номер'
unsuccessful_find_number_offer_other_text = '😥 Не удалось найти номер\n' \
                                            'Искать номер с более высокой ценой?'

success_find_price_number_text = '💰 Ваш баланс: <b>{balance}</b> RUB\n\n' \
                                 '⚙️ Сервис: {service_name}\n' \
                                 '🚩 Страна: {country_international_code}\n' \
                                 '🌐 Оператор: {operator_name}\n' \
                                 '💸 Стоимость: {price} RUB\n' \
                                 '🔍 Количество: {count}'

finding_number_text = 'Ищу номер⏳'

# success_find_number_text = f'📱 Ваш номер: {hcode("{number}")}'
success_find_number_text = f'📱 Ваш номер: {hcode("{number}")}\n\n' \
                           '📫 Ожидает сообщение\n' \
                           '✅ Подтвердите кнопкой, когда смс будет отправлено на номер (необязательно)\n' \
                           '📆 Последнее обновление: {last_update}'

success_find_number_text_after_confirm = f'📱 Ваш номер: {hcode("{number}")}\n\n' \
                                         '📫 Ожидает сообщение\n' \
                                         '📆 Последнее обновление: {last_update}'

number_code_and_message_text = f'📱 Ваш номер: {hcode("{number}")}\n\n' \
                               f'💬 Код: {hcode("{sms}")}\n' \
                               '✉️ Полное сообщение:\n{full_sms}'

cant_repeat_number_message_text = '😓 На данный номер больше нельзя принять сообщение'

cancel_number_text = '❌ Номер отменен\n\n' \
                     '💰 Ваш баланс: <b>{balance}</b> RUB'
success_end_number_text = '✔️ Активация успешно завершена\n\n' \
                          '💰 Ваш баланс: <b>{balance}</b> RUB'

max_favorites_count_text = '⚠ Достигнуто максимальное количество {max_count} в избранном'
already_in_favorites_text = '⭐ Уже в избранном'
success_add_to_favorites_text = '✔️ Добавлено в избранное'
no_favorite_text = '😯 У вас еще нет избранного'

not_enough_balance_text = '🚫 У вас недостаточно средств на балансе'

end_number_time_activation_text = '⌛ Время активации завершено'

find_countries_prices_text = 'Смотрю цены 👀'
rent_menu_text = '📲 Меню аренды'

choose_rent_duration_text = '⏱️ Выберите длительность аренды'
hours_rent_duration_text = '⏱️ На сколько часов необходимо арендовать номер?'
days_rent_duration_text = '⏱️ На сколько дней необходимо арендовать номер?\n' \
                          'Максимальная длительность аренды 56 дней'
bad_rent_hours_duration_format_text = '❌ Неверный формат. Можно выбрать только из {hours_values} значений'
bad_rent_days_hours_duration_format_text = '❌ Неверный формат.\n' \
                                           'Максимальная длительность аренды 56 дней'

find_rent_services_text = '👀 Подбираю сервисы с арендой на {rent_duration}ч.'

rent_success_find_number_text = f'📱 Ваш номер: {hcode("{number}")}\n' \
                                'Все данные по этому номеру можно найти в меню аренды'

no_rent_numbers_text = '😯 У вас еще нет номеров в аренде'
choose_rent_number_text = '📱 Выберите арендованный номер'

no_rent_history_text = '📁 У вас еще нет истории'

rent_number_full_history_info_text = f'📱 Номер: {hcode("{number}")}\n' \
                                     '⚙️ Сервис: {service_name}\n' \
                                     '🚩 Страна: {country_international_code}\n' \
                                     '🌐 Оператор: {operator_name}\n' \
                                     '📆 Дата начала аренды: {created_at}\n' \
                                     '📆 Дата окончания аренды: {end_date}\n\n'

rent_history_is_big_text = '...\n\n\n' \
                           '<b>Ваша история большая и превышает лимит отправки тг в одном сообщении.\n' \
                           'Отправить полную историю несколькими сообщениями?</b>'

rent_number_full_info_text = f'📱 Номер: {hcode("{rent_number}")}\n' \
                             '⚙️ Сервис: {service_name}\n' \
                             '🚩 Страна: {country_international_code}\n' \
                             '🌐 Оператор: {operator_name}\n' \
                             '📆 Дата окончания аренды: {end_date}'

rent_number_info_text = f'📱 Номер: {hcode("{rent_number}")}\n' \
                        '⚙️ Сервис: {service_name}\n' \
                        '🚩 Страна: {country_international_code}\n' \
                        '🌐 Оператор: {operator_name}'

end_rent_number_text = '✔️ Номер завершен'

number_wait_message_text = '📫 Ожидает сообщение'

rent_number_message_text = f'От: {hbold("{phone_from}")}\n' \
                           'Когда: {date}\n' \
                           'Текст: {text}'

online_sim_bad_cancel_number_text = '😵‍💫 Для данного номера завершение операции возможно через 2 минуты после заказа ' \
                                    'номера или после прихода смс'

sms_actiwator_sim_bad_cancel_number_text = '😵‍💫 Для данного номера возврат возможен не ранее чем через ' \
                                           '30 секунд после покупки'
