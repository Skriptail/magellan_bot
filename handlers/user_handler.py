import json

from aiogram import Bot, Dispatcher, F, Router, types
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, FSInputFile

from filters import ChatTypeFilter
from keyboards import (
    add_goal_kb,
    intro_kb,
    price_kb,
    reset_goal_kb,
)

user_router = Router()
user_router.message.filter(ChatTypeFilter(["private"]))

class AddUser(StatesGroup):
    name = State()
    amount_of_guests = State()
    time = State()
    phone_number = State()
    number_of_table = State()

    last_message = State()

@user_router.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(
        f"Привет, {message.from_user.first_name}! Я Бот лаундж-бара Magellan. Здесь можно забронировать столик, посмотреть меню, оставить отзыв и чаевые :)",
        reply_markup=intro_kb)


# роутер для отлова коллбека бронирования столика и последующей записи
@user_router.callback_query(F.data == "book")
async def add_goal(callback_query: types.CallbackQuery, state: FSMContext):
    sent_message = await callback_query.message.edit_text("Введите свое имя: ", reply_markup=add_goal_kb)
    await state.update_data(last_message_id=sent_message.message_id)  # сохраняем ID предыдущего сообщения в FSM
    await state.set_state(AddUser.name)


# роутер для выбора количества гостей
@user_router.message(AddUser.name)
async def add_amount_of_guests(message: types.Message, state: FSMContext, bot: Bot):
    await state.update_data(name=message.text)
    await message.delete()
    data = await state.get_data()
    last_message_id = data.get('last_message_id')

    await bot.edit_message_text(f"Имя: {data['name']}\n"
                                "Введите количество персон: ",
                                chat_id=message.chat.id,
                                message_id=last_message_id,
                                reply_markup=add_goal_kb)
    await state.set_state(AddUser.amount_of_guests)


# роутер для времени
@user_router.message(AddUser.amount_of_guests)
async def add_name(message: types.Message, bot: Bot, state: FSMContext):
    await state.update_data(amount_of_guests=message.text)
    await message.delete()
    data = await state.get_data()
    last_message_id = data.get('last_message_id')

    await bot.edit_message_text(f"Имя: {data['name']}\n"
                                f'Количество персон: {data["amount_of_guests"]}\n'
                                "Укажите удобное Вам время: ",
                                chat_id=message.chat.id,
                                message_id=last_message_id,
                                reply_markup=add_goal_kb)

    await state.set_state(AddUser.time)


# роутер для телефона
@user_router.message(AddUser.time)
async def add_name(message: types.Message, bot: Bot, state: FSMContext):
    await state.update_data(time=message.text)
    await message.delete()
    data = await state.get_data()
    last_message_id = data.get('last_message_id')

    await bot.edit_message_text(f"Имя: {data['name']}\n"
                                f'Количество персон: {data["amount_of_guests"]}\n'
                                f'Время: {data["time"]}\n'
                                "Введите номер телефона для связи: ",
                                chat_id=message.chat.id,
                                message_id=last_message_id,
                                reply_markup=add_goal_kb)

    await state.set_state(AddUser.phone_number)


# роутер для выбора места
@user_router.message(AddUser.phone_number)
async def add_phone_number(message: types.Message, bot: Bot, state: FSMContext):
    await state.update_data(phone_number=message.text)
    await message.delete()
    data = await state.get_data()
    last_message_id = data.get('last_message_id')

    await bot.edit_message_text(f"Имя: {data['name']}\n"
                                f"Количество персон: {data['amount_of_guests']}\n"
                                f'Время: {data["time"]}\n'
                                f"Номер телефона: {data['phone_number']}\n"
                                "Выберите подходящее вам место(например: 1 стол): ",
                                chat_id=message.chat.id,
                                message_id=last_message_id,
                                reply_markup=price_kb)

    await state.set_state(AddUser.number_of_table)


@user_router.callback_query(F.data.startswith('numberoftable'))
async def add_number_of_table(callback_query: types.CallbackQuery, bot: Bot, state: FSMContext):
    selected_number_of_table = callback_query.data.split("_")[1]
    await state.update_data(number_of_table=selected_number_of_table)
    data = await state.get_data()
    last_message_id = data.get('last_message_id')
    other_user_chat_id = 485061270

    await bot.edit_message_text(f"Ваше имя: {data['name']}\n"
                                f"Количество персон: {data['amount_of_guests']}\n"
                                f'Время: {data["time"]}\n'
                                f"Номер телефона: {data['phone_number']}\n"
                                f"Выбранное место: {data['number_of_table']}\n",
                                chat_id=callback_query.message.chat.id,
                                message_id=last_message_id,
                                reply_markup=reset_goal_kb)

    await bot.send_message(
        other_user_chat_id,
        'Данные из бота:\n'
        f'Имя: {data["name"]}\n'
        f'Время: {data["time"]}\n'
        f'Количество гостей: {data["amount_of_guests"]}\n'
        f'Номер телефона: {data["phone_number"]}\n'
        f'Номер стола: {data["number_of_table"]}\n')


@user_router.callback_query(F.data == "rules")
async def answer(callback_query: types.CallbackQuery, bot: Bot):
    global previous_bot_message
    await bot.send_message(callback_query.from_user.id, """⚜️ Правила MAGELLAN Lounge-bar ⚜️

Дорогие гости, в нашем заведении царит атмосфера комфорта. Ради того, чтобы ничего не помешало вам наслаждаться посещением, разработана система правил:

🔸При посещении лаунж-бара, заказ кальяна обязателен (1 кальян на компанию до 4-х гостей, 2 кальяна на 5-6 гостей, 3 кальяна для 7-ми человек)

🔸При бронировании VIP-комнаты с Playstation  количество кальянов кратно 1 на 2 гостя. Замена кальяна через 1,5 часа с момента выноса.

🔸Мы придерживаемся взаимного уважения, поэтому, с заботой о других гостях, просим вас проявлять эмоции не громко.

🔸Возможно заказать доставку еды, мы поможем вам с сервировкой.

🔸За порчу имущества заведения предусмотрена система штрафов (список штрафов предоставлен в документах заведения).

🔸Инвалиды и люди с ограниченными возможностями обслуживаются вне очереди.

❌ Запрещено посещение заведения лицами до 18 лет, при запросе персоналом вашего паспорта - оригинал обязателен.

❌ Запрещено посещение заведения в состоянии наркотического, сильного алкогольного опьянения.

❌ Запрещено курение сигарет, сигарилл, сигар, самокруток, употребление наркотических веществ.

❌ Вход со своим алкоголем и напитками запрещен, предоставляем вам широкий ассортимент напитков, алкогольной, винной и коктейльной карты.

❌ Запрещено посещение гостевого санузла, если вы не являетесь гостем нашего заведения.

❌ Запрещено агрессивное поведение и выражение неуважения гостям и персоналу заведения. При угрозе личной безопасности, персонал заведения имеет право вызвать Охранную Организацию.

❌ Запрещено присвоение имущества заведения. За присвоение зарядных устройств, элементов декора и пр. - взымается плата в размере полной закупочной стоимости.

📍За несоблюдение правил, после вежливого замечания, персонал уполномочен попросить вас покинуть заведение.📍

🎥 Внимание. Ведётся видео-фиксация. 🎥

Приятного и безопасного отдыха,
🖤 Ваш MAGELLAN! 🖤 """)

# роутер для отлова коллбека по меню
@user_router.callback_query(StateFilter("*"), F.data == "menu")
async def menu(callback_query: types.CallbackQuery, state: FSMContext, bot: Bot):
    global previous_bot_message
    message = callback_query.message
    photo_path = "magellanbot/app/static/he.jpg"

    with open(photo_path, 'rb') as photo:
        photo_file = FSInputFile("magellanbot/app/static/menu1.jpg")
        await bot.send_photo(callback_query.from_user.id, photo_file, caption='Ниже представлены позиции меню:')

# коллбек для возврата на главную страницу
@user_router.callback_query(F.data == "back_to_main")
async def add_goal(callback_query: types.CallbackQuery, state: FSMContext):
    global previous_bot_message

    await callback_query.message.edit_text("Вы вернулись на главную", reply_markup=intro_kb)

    # @user_router.message(F.data.second_step)
    # async def add_number_of_table_message(message: types.Message, bot: Bot, state: FSMContext):
    #     await message.delete()
    #     data = await state.get_data()

    await state.clear()

