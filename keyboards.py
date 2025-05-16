from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType

reply_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
    KeyboardButton(text='Ряд 1 Кнопка 1'),
    KeyboardButton(text='Ряд 1 Кнопка 2'),
],
[
    KeyboardButton(text='Ряд 2 Кнопка 1'),
    KeyboardButton(text='Ряд 2 Кнопка 2'),
]
],
resize_keyboard=True, input_field_placeholder='выберите кнопку', one_time_keyboard=True
)


loc_tel_poll_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Отправить геолокацию',
            request_location=True
        )
    ],
    [
        KeyboardButton(
            text='Отправить contact',
            request_contact=True
        )
    ],
    [
        KeyboardButton(
            text='Создать викторину',
            request_poll=KeyboardButtonPollType(type='regular')
        )
    ],
],
resize_keyboard=True, input_field_placeholder='', one_time_keyboard=False)