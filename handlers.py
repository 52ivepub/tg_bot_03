import datetime
import json
import os
from aiogram import F, Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import FSInputFile, Message, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.chat_action import ChatActionSender
from apscheduler.jobstores.redis import RedisJobStore 
from aiogram.methods.send_message import SendMessage
from keyboards import (
    reply_keyboard,
    loc_tel_poll_keyboard,
    inline_keys,
    get_inlineKeyboardBuilder,
    send_file_keyboard
)
from middleware import OfficeHoursMiddleware, CounterMiddleware, SchedulerMiddleware
from db_connect import Request
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler_di import ContextSchedulerDecorator
all_media_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media')


jobstores = {
    'default': RedisJobStore(jobs_key='dispatched_trips_jobs',
                             run_times_key='dispatched_trips_running',
                             host='localhost',
                             db=2,
                             port=6379)
}
scheduler = ContextSchedulerDecorator(AsyncIOScheduler(jobstores=jobstores))



handler = Router()

handler.message.middleware(CounterMiddleware())
# handler.message.middleware(OfficeHoursMiddleware())   # обрабатывает время когда бот может отвечать
handler.message.middleware(SchedulerMiddleware(scheduler))


class StepsForm(StatesGroup):
    GET_NAME = State()
    GET_LAST_NAME = State()
    GET_AGE = State()


# async def send_interval(bot: Bot):
#     await bot.send_message(1301478301, 'это сообщение будет приходить каждые 15 секунд')

async def send_date(bot: Bot):
    await bot.send_message(1301478301, 'Ваши данные внесены в базу')



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
    scheduler.ctx.add_instance(bot, declared_class=Bot)
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

@handler.message(Command("files"))
async def start(message: Message):
    await message.answer("вот еще клавиатура", reply_markup=send_file_keyboard)



@handler.message(F.text.lower().contains("отправить фото"))
async def start(message: Message):
    photo_file = FSInputFile(path=os.path.join(all_media_dir, 'sticker.webp'))
    msg_id = await message.answer_photo(photo=photo_file, 
                                        caption='Моя <u>отформатированная</u> подпись к <b>фото</b>')
    print(msg_id.photo[-1].file_id)

@handler.message(F.text.lower().contains("отправить аудио"))
async def start(message: Message, bot: Bot):
   async with ChatActionSender.upload_voice(bot=bot, chat_id=message.from_user.id): 
        audio_file = FSInputFile(path=os.path.join(all_media_dir, 'audio.mp3'))
        msg_id = await message.answer_audio(audio=audio_file, 
                                            caption="<tg-spoiler><b>Ты супер</b></tg-spoiler>\n")
        print(msg_id.audio.file_id)
    

@handler.message(F.photo)
async def get_photo(message: Message, bot: Bot):
    file = await bot.get_file(message.photo[-1].file_id)
    await message.answer("Получено фото")
    await bot.download_file(file.file_path, f"media/photo{message.photo[-1].file_id[:5]}.jpg")

