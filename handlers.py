import json
from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from keyboards import (
    reply_keyboard,
    loc_tel_poll_keyboard,
    inline_keys,
    get_inlineKeyboardBuilder,
)
from middleware import OfficeHoursMiddleware, CounterMiddleware
from db_connect import Request



handler = Router()

handler.message.middleware(CounterMiddleware())
# handler.message.middleware(OfficeHoursMiddleware())   # обрабатывает время когда бот может отвечать



@handler.message(Command("start"))
async def start(message: Message, counter: str, request: Request):
    await request.add_data(message.from_user.id, message.from_user.first_name)

    await message.answer(f"сообщение # {counter}")
    await message.answer("привет", reply_markup=reply_keyboard)


@handler.message(Command("inline"))
async def start(message: Message):
    await message.answer("вот инлайн", reply_markup=inline_keys)


@handler.message(Command("bilder"))
async def start(message: Message):
    await message.answer("вот bilder", reply_markup=get_inlineKeyboardBuilder())


@handler.callback_query(F.data.contains("iphone_"))
async def callback_send(call: CallbackQuery):
    await call.answer()
    num = call.data[-1]
    await call.message.answer(f"Вы запросили iphone_{num}")


@handler.message(Command("help"))
async def start(message: Message):
    await message.answer("вот другая клавиатура", reply_markup=loc_tel_poll_keyboard)


@handler.message(F.text.lower().contains("прив"))
async def start(message: Message):
    await message.reply(f"<b>И тебе привет {message.from_user.first_name}</b>")
    print({json.dumps(message.dict(), default=str)})


@handler.message(F.photo)
async def get_photo(message: Message, bot: Bot):

    file = await bot.get_file(message.photo[-1].file_id)
    await message.answer("Получено фото")
    await bot.download_file(
        file.file_path, f"media/photo{message.photo[-1].file_id[:5]}.jpg"
    )
