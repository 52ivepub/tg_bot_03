import os
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv, find_dotenv
from aiogram.types import Message
from aiogram import Bot, Dispatcher
import asyncio
from handlers import handler
import logging

load_dotenv(find_dotenv())


async def start(bot: Bot):
    await bot.send_message(chat_id=os.getenv("CHAT_ID"), text='бот запущен')

async def stop(bot: Bot):
    await bot.send_message(chat_id=os.getenv("CHAT_ID"), text='бот остановлен')

bot = Bot(token=os.getenv("TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
dp.include_router(handler)

async def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(name)s - '
    '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s')
                        
    dp.startup.register(start)
    dp.shutdown.register(stop)
    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())