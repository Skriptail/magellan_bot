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

previous_bot_message = None


# class TgHandler:
#     async def cloud_run(self, event):
#         for message in event["messages"]:
#             message_body = json.loads(message["details"]["message"]["body"])

#             update = types.Update(**message_body)


class ProcessState(StatesGroup):
    first_step = State()
    second_step = State()


class AddUser(StatesGroup):
    name = State()
    amount_of_guests = State()
    time = State()
    phone_number = State()
    number_of_table = State()

    last_message = State()

    texts = {
        'AddUser:name': 'Введите имя заново:',
        'AddUser:phone_number': 'Введите номер телефона заново:',
        'AddUser:number_of_table': 'Введите тариф заново:',
    }


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
    #  485061270 me
    # 6121957414 2 me
    # 1271362249
    # магеллан - 670580354
    await bot.edit_message_text(f"Ваше имя: {data['name']}\n"
                                f"Количество персон: {data['amount_of_guests']}\n"
                                f'Время: {data["time"]}\n'
                                f"Номер телефона: {data['phone_number']}\n"
                                f"Выбранное место: {data['number_of_table']}\n",
                                chat_id=callback_query.message.chat.id,
                                message_id=last_message_id,
                                reply_markup=reset_goal_kb)
    # last_message_id = callback_query.message.chat.id
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
    await bot.send_message(callback_query.from_user.id, "Правила нашего бара:\n"
                                                        "1. нельзя пить\n"
                                                        "2. нельзя курить\n"
                                                        "3. нельзя спорить с артуром\n")


@user_router.callback_query(StateFilter("*"), F.data == "cancel")
async def cancel(callback_query: types.CallbackQuery, state: FSMContext):
    global previous_bot_message

    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    # await callback_query.message.edit_text("Действие отменено", reply_markup=add_goal_kb)
    await answer(callback_query.message)


@user_router.callback_query(StateFilter("*"), F.data == "back")
async def cancel(callback_query: types.CallbackQuery, state: FSMContext):
    global previous_bot_message

    current_state = await state.get_state()

    if current_state == AddUser.name:
        await state.clear()
        # await callback_query.message.edit_text("Действие отменено", reply_markup=add_goal_kb)
        await answer(callback_query.message)

    previous_state = await state.get_state()
    for step in AddUser.__all_states__:
        if step.state == current_state:
            await state.set_state(previous_state)
            await callback_query.message.edit_text(
                f"Вы вернулись к прошлому шагу \n{AddUser.texts[previous_state.state]}", reply_markup=add_goal_kb)
        previous_state = step


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

