import json
from aiogram import F, Router, Bot
from aiogram.types import Message
from aiogram.filters import Command




handler = Router()

@handler.message(Command('start'))
async def start(message: Message):
    await message.answer('привет')

@handler.message(F.text.lower().contains('прив'))
async def start(message: Message):
    await message.reply(f'<b>И тебе привет {message.from_user.first_name}</b>')
    print({json.dumps(message.dict(), default=str)})


@handler.message(F.photo)
async def get_photo(message:Message, bot: Bot):
    
    file = await bot.get_file(message.photo[-1].file_id)
    await message.answer('Получено фото')
    await bot.download_file(file.file_path, f'media/photo{message.photo[-1].file_id[:5]}.jpg')

    
