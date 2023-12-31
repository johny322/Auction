start_user_message_text = '👋 Добро пожаловать!\n' \
                          '<a href="{reserve_chanel_url}">Резервный Канал</a>\n' \
                          '<a href="{news_chanel_url}">Новостной Канал</a>\n' \
                          '<a href="{main_chanel_url}">Аукцион</a>\n'

profile_message_text = 'ID: {id}\n' \
                       'Баланс: {balance} руб\n' \
                       'Выиграно аукционов: {wins_count}\n' \
                       'Выплачено: {paid_balance} руб'

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

anti_flood_message_text = '‼️ Не спамь! Перерыв {}с'

####################################
empty_text = '⠀'

# auction

join_main_chanel_message_text = """
🔴 Вас нет в канале аукциона, вступите туда, чтобы пользоваться ботом

Ссылка на вступление: {main_chanel_url}
"""

join_main_chanel_query_text = """
🔴 Вас нет в канале аукциона, вступите туда, чтобы пользоваться ботом
"""

auction_start_message_text = 'Аукцион  ✈️\n' \
                             'Правила аукциона:️\n' \
                             '▫️ Любой участник может начать аукцион нажав кнопку Начать аукцион️\n' \
                             '▫️ Аукцион может быть завершен при достижении от 2 ставок️\n' \
                             '▫️ Любой участник может повысить предыдущую ставку и стать лидером️\n' \
                             '▫️ Максимальный шаг повышения - 10 рублей️\n' \
                             '▫️ После повышения ставки аукцион продлевается на 8 минут️\n' \
                             '▫️ Как только таймер доходит до нуля, деньги зачисляются тому, кто сделал последнюю ставку️\n' \
                             '▫️ Пользователь не может сделать более одной ставки подряд️\n' \
                             '▫️ На момент завершения аукциона, победитель получает {winner_persent}% суммы от всех ставок аукциона на счет для вывода️\n' \
                             '▫️ Если ставка единственная (никто не перебил стартовую ставку) аукцион завершится через 12 часов, открывшему начисляется {only_one_winner_persent}%️\n' \
                             '▫️ Для того чтобы пополнить баланс, перейдите в бот и нажмите кнопку: Личный Кабинет > 💳 Пополнить\n' \
                             '▫️ Для того чтобы произвести вывод, перейдите в бот и нажмите кнопку: Личный Кабинет > Вывод'
minimal_auction_bet_warning_text = '🤔 У вас недостаточно баланса для минимальной ставки ({} руб)'
auction_first_bet_message_text = '💳 Ваш баланс: <b>{balance}</b> руб\n\n' \
                                 'Отправьте размер первой ставки целым числом\n' \
                                 'Например: 100'
bad_first_bet_message_text = '😧 Неверный формат'
no_balance_message_text = '🤔 У вас недостаточно баланса для такой ставки'
minimal_bet_size_warning_text = '❗ Минимальный размер ставки {} руб'
cant_bet_two_times_message_text = '❗ Вы не можете делать ставку два раза подряд'
confirm_bet_size_message_text = 'Вы хотите начать аукцион со ставки в размере <b>{}</b> руб?'
auction_already_has_message_text = '😧 Сейчас уже идет аукцион'
no_auction_already_has_message_text = '😧 Сейчас нет активного аукциона'
has_bet_lager_than_message_text = '😧 Текущая ставка {} больше вашей. Выберите другую ставку'
start_auction_message_text = 'Пользователь {full_name} | @{username} начал аукцион с начальной ставкой {bet_size}'
new_bet_auction_message_text = '👨🏻‍⚖️ Аукцион №{auction_id}\n\n' \
                               '⏱ Осталось: {time_to_end}\n' \
                               '💰 Банк аукциона: {full_bet_sum} руб\n' \
                               '🔨 Количество ставок: {bets_count}\n\n' \
                               '👑 Лидер: {full_name} | @{username} поставил(а) {last_bet_sum} руб!\n\n' \
                               '👇 Выберете количество рублей для повышения ставки:'

good_start_auction_message_text = '🚀 Вы создали <a href="{}">аукцион</a>'

balance_message_text = '💰 Баланс: {} руб'
end_auction_message_text = '👨🏻‍⚖️ Аукцион завершён!\n\n' \
                           '👑 Лидер: {full_name} | @{username}, победил ставкой {last_bet_sum} рублей!\n\n' \
                           '🎲 Количество ставок за игру: {bets_count}\n' \
                           '💰 Банк аукциона: {full_bet_sum} рублей\n' \
                           '💳 Победитель получает {winner_percent}% от банка аукциона - {user_win_sum} руб\n\n' \
                           '🕐 Время окончания: {end_date} по МСК\n' \
                           '⌛️ Длительность аукциона: {auction_time} мин'
new_bet_user_alert_message_text = '😧 Вышу ставку перебили\n' \
                                  '💸 Новая ставка: {} руб'
auction_winner_message_text = '🤜 Вы победили в аукционе!\n' \
                              '💸 На ваш баланс зачислено {user_win_sum} руб'
add_auction_message_text = '<a href="https://telegra.ph/Svoj-Aukcion-12-18">Подкл Аукцион</a>\n' \
                           'Ваш Процет - 9% с каждого Лота\n' \
                           'По Вопросам - @yeah_end'
need_bot_sub_query_text = 'Вы не запускали нашего бота. Воспользуйтесь кнопкой 🔗 Перейти в бот'
return_auction_bets_message_text = 'Ваши ставки за аукцион №{auction_id} были возвращены ({bets_size} руб)'
good_return_auction_bets_message_text = 'Ставки за аукцион №{auction_id} были возвращены\nЧисло людей: {users_count}'

##############
info_reserve_chanel_message_text = '🗿 <a href="{reserve_chanel_url}">Резервный Канал</a>'
info_main_chanel_message_text = '💰 <a href="{main_chanel_url}">Аукцион</a>'
info_payout_chanel_message_text = '💸 <a href="{payout_chanel_url}">Выплаты</a>'
info_news_chanel_message_text = '📰 <a href="{news_chanel_url}">Новостной Канал</a>'

auction_rules_text = '1. https://telegra.ph/Obshchee-polozhenie-12-18\n' \
                     '2. https://telegra.ph/Pravila-Aukciona-12-18-2'
bot_rules_text = '1. https://telegra.ph/Obshchee-Polozhenie-12-18-2\n' \
                 '2. https://telegra.ph/Svoj-Aukcion-12-18'
recommend_message_text = '<a href="https://t.me/Spanch_Proxy_Bot">Прокси</a>\n' \
                         '<a href="https://t.me/SMS_Spanch_Bot">Прием смс</a>\n' \
                         '<a href="https://t.me/Shop_Spanch_Bot">Шоп</a>\n'
