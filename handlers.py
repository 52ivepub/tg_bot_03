import json
from aiogram import F, Router, Bot
from aiogram.types import Message
from aiogram.filters import Command
from keyboards import reply_keyboard, loc_tel_poll_keyboard




handler = Router()

@handler.message(Command('start'))
async def start(message: Message):
    await message.answer('привет', reply_markup=reply_keyboard)
    
@handler.message(Command('help'))
async def start(message: Message):
    await message.answer('вот другая клавиатура', reply_markup=loc_tel_poll_keyboard)

    

@handler.message(F.text.lower().contains('прив'))
async def start(message: Message):
    await message.reply(f'<b>И тебе привет {message.from_user.first_name}</b>')
    print({json.dumps(message.dict(), default=str)})


@handler.message(F.photo)
async def get_photo(message:Message, bot: Bot):
    
    file = await bot.get_file(message.photo[-1].file_id)
    await message.answer('Получено фото')
    await bot.download_file(file.file_path, f'media/photo{message.photo[-1].file_id[:5]}.jpg')

    
