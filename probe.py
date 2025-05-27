

import asyncio
import os
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import asyncpg
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

bot = Bot(token=os.getenv("TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))

async def send(bot: Bot):
    await bot.send_message(1301478301, 'это сообщение придет через 10')

asyncio.run(send(bot=bot))