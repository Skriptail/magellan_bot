import asyncio
from aiogram import Bot, Dispatcher, types
from handlers.user_handler import user_router
from commands import private


BOT_TOKEN = ''


bot = Bot(token=(BOT_TOKEN))

dp = Dispatcher()

dp.include_router(user_router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot)


if "__main__" == __name__:
    asyncio.run(main())