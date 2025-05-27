import datetime
import json
from aiogram import F, Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.methods.send_message import SendMessage
from keyboards import (
    reply_keyboard,
    loc_tel_poll_keyboard,
    inline_keys,
    get_inlineKeyboardBuilder,
)
from middleware import OfficeHoursMiddleware, CounterMiddleware, SchedulerMiddleware
from db_connect import Request
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()

handler = Router()

handler.message.middleware(CounterMiddleware())
# handler.message.middleware(OfficeHoursMiddleware())   # обрабатывает время когда бот может отвечать
handler.message.middleware(SchedulerMiddleware(scheduler))


class StepsForm(StatesGroup):
    GET_NAME = State()
    GET_LAST_NAME = State()
    GET_AGE = State()


async def send_interval(bot: Bot):
    await bot.send_message(1301478301, 'это сообщение будет приходить каждые 15 секунд')

async def send_date(bot: Bot):
    await bot.send_message(1301478301, 'это сообщение придет ОДИН раз через 5 секунд')



@handler.message(Command("start"))
async def start(message: Message, counter: str, bot: Bot):
    await message.answer(f"сообщение # {counter}")
    await message.answer("привет")
    
    # ===========ПЛАНИРОВЩИК ЗАДАЧ============
    # scheduler = AsyncIOScheduler()   
    # scheduler.add_job(send_interval, 'interval', seconds=15, kwargs={'bot': bot})
    # scheduler.add_job(send_date, 'date', run_date=datetime.datetime.now() + datetime.timedelta(seconds=5), kwargs={'bot': bot})
    # scheduler.start()
         





@handler.message(Command("inline"))
async def start(message: Message):
    await message.answer("вот инлайн", reply_markup=inline_keys)


@handler.message(Command("form"))
async def form(message: Message, state: FSMContext):
    await message.answer(f'{message.from_user.first_name}, начинаем заполнять. Введите имя')
    # await state.update_data(GET_NAME=message.text)
    await state.set_state(StepsForm.GET_NAME)


@handler.message(StepsForm.GET_NAME)
async def start(message: Message, state: FSMContext):
    await message.answer(f'Твое имя:\r\n{message.text}\r\nТеперь фамилию')
    await state.update_data(name=message.text)
    await state.set_state(StepsForm.GET_LAST_NAME)


@handler.message(StepsForm.GET_LAST_NAME)
async def start(message: Message, state: FSMContext):
    await message.answer(f'Твоя фамилия: {message.text} Теперь возраст')
    await state.update_data(last_name=message.text)
    await state.set_state(StepsForm.GET_AGE)
    

@handler.message(StepsForm.GET_AGE)
async def start(message: Message, state: FSMContext, 
                request: Request, scheduler: AsyncIOScheduler, bot: Bot):
    await message.answer(f'Твой возраст: {message.text} ')
    await state.update_data(age=message.text)
    context_data = await state.get_data()
    await message.answer(f"Имя: {context_data.get('name')}\n"
    f"Фамилия: {context_data.get('last_name')}\n"
    f"Возраст: {context_data.get('age')}")
    await request.add_data(first_name=context_data.get('name'), last_name=context_data.get('last_name'), age=context_data.get('age'))
    await state.clear() 
    scheduler.add_job(send_date, 'date', 
                      run_date=datetime.datetime.now() + datetime.timedelta(seconds=5), kwargs={'bot': bot})
    scheduler.start()   


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
    await bot.download_file(file.file_path, f"media/photo{message.photo[-1].file_id[:5]}.jpg")

