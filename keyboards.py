from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



intro_kb = InlineKeyboardMarkup(
    inline_keyboard=[
            [
                InlineKeyboardButton(text='Забронировать столик', callback_data='book'),
                InlineKeyboardButton(text='Меню', callback_data='menu'),
                InlineKeyboardButton(text='Оставить отзыв', callback_data='feedback'),
                InlineKeyboardButton(text='Оставить чаевые', callback_data='tip'),
                InlineKeyboardButton(text='Правила', callback_data='rules')
            ]
        ]
)

add_goal_kb = InlineKeyboardMarkup(
    inline_keyboard=[
            [
                InlineKeyboardButton(text='Назад', callback_data='back_to_main'),
            ]
        ]
)

reset_goal_kb = InlineKeyboardMarkup(
    inline_keyboard=[
            [
                InlineKeyboardButton(text='Готово!✅ С вами свяжется наш менеджер, хорошего дня!', callback_data='done'),
            ]
        ]
)
price_kb = InlineKeyboardMarkup(
    inline_keyboard=[
                [InlineKeyboardButton(text='1 стол у окна', callback_data='numberoftable_1')],
                [InlineKeyboardButton(text='2 стол у окна', callback_data='numberoftable_2')],
                [InlineKeyboardButton(text='3 стол у окна', callback_data='numberoftable_3')],
                [InlineKeyboardButton(text='4 стол', callback_data='numberoftable_4')],
                [InlineKeyboardButton(text='5 стол у колонны', callback_data='numberoftable_5')],
                [InlineKeyboardButton(text='6 стол у колонны', callback_data='numberoftable_6')],
                [InlineKeyboardButton(text='1 VIP', callback_data='numberoftable_VIP1')],
                [InlineKeyboardButton(text='2 VIP', callback_data='numberoftable_VIP2')],
                [InlineKeyboardButton(text='Назад', callback_data='back_to_main')],
    ]
)
sub_price_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='4 занятия - 2700₽', callback_data=f'tarif_abon1')],
        [InlineKeyboardButton(text='8 занятий - 5000₽', callback_data='tarif_abon2'),],
        [InlineKeyboardButton(text='12 занятий - 6900₽', callback_data='tarif_abon3')],
        [InlineKeyboardButton(text='Записаться на занятие', callback_data='book')],
        [InlineKeyboardButton(text='Назад', callback_data='back_to_main')]
    ]
)
select_numberoftable__kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Разовое занятие  - 800₽', callback_data='tarif_1'),],
        [InlineKeyboardButton(text='Первое пробное  - 600₽', callback_data='tarif_1'),],
        [InlineKeyboardButton(text='Абонементы', callback_data='abonements')],
        [InlineKeyboardButton(text='Назад', callback_data='back_to_main')]
    ]
)