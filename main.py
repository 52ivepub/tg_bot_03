import os
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv, find_dotenv
from aiogram.types import Message
from aiogram import Bot, Dispatcher
import asyncio
from commands import set_commands
from handlers import handler
import logging
from db_connect import Request, DbSession
import asyncpg

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
    await set_commands(bot)                
    dp.startup.register(start)
    dp.shutdown.register(stop)
    # pool_connect = await asyncpg.create_pool(user='postgres', password='1', database='bot', 
                                            #  host='127.0.0.1', port=5432, command_timeout=60)
    # dp.update.middleware.register(DbSession(pool_connect))
    await dp.start_polling(bot)
   



if __name__ == "__main__":
    asyncio.run(main())