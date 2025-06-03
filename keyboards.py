from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
 KeyboardButtonPollType, InlineKeyboardButton, InlineKeyboardMarkup)

from aiogram.utils.keyboard import InlineKeyboardBuilder

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

send_file_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Отправить фото',
        )
    ],
    [
        KeyboardButton(
            text='Отправить аудио',
            
        )
    ],
    [
        KeyboardButton(
            text='Отправить эмоджи',
            
        )
    ],
],
resize_keyboard=True, input_field_placeholder='', one_time_keyboard=False)

# ==========INLINE===============

inline_keys = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Iphone 5', 
                            callback_data='iphone_5')
    ],
    [
        InlineKeyboardButton(text='Iphone 6', 
                            callback_data='iphone_6')
    ],
    [
        InlineKeyboardButton(text='Iphone 7', 
                            callback_data='iphone_7')
    ],
    [
        InlineKeyboardButton(text='Iphone 6', 
                            url='https://novosibirsk.drom.ru/')
    ],
])



# ==========InlineKeyboardBuilder===========


def get_inlineKeyboardBuilder():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='IPHONE 5', callback_data='iphone_5')
    keyboard_builder.button(text='IPHONE 6', callback_data='iphone_6')
    keyboard_builder.button(text='IPHONE 7', callback_data='iphone_7')

    keyboard_builder.adjust(2,1)
    return keyboard_builder.as_markup()