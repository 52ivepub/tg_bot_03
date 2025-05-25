from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.fsm.context import FSMContext


class StepsForm(StatesGroup):
    GET_NAME = State()


async def get_form(message: Message, state: FSMContext):
    await message.answer(f'{message.from_user.first_name}, начинаем заполнять. Введите имя')
    await state.set_state(StepsForm.GET_NAME)


async def get_name(message: Message):
    await message.answer(f'Твое имя:\r\n{message.text}\r\nТеперь фамилию')

