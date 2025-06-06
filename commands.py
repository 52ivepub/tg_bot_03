from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start', description='Старт'
        ),
        BotCommand(
            command='help', description='Помощь'
        ),
        BotCommand(
            command='inline', description='inline'
        ),
        BotCommand(
            command='bilder', description='bilder'
        ),
        BotCommand(
            command='form', description='Начать опрос'
        ),
        BotCommand(
            command='files', description='отправить'
        ),
        
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())


