import asyncpg
from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from typing import Dict, Any, Callable, Awaitable


class Request:
    def __init__(self, connector: asyncpg.pool.Pool):
        self.connector = connector

    async def add_data(self, user_id, user_name):
        query = f"INSERT INTO dateuser (user_id, user_name) VALUES ({user_id}, '{user_name}')"\
                
        await self.connector.execute(query)


class DbSession(BaseMiddleware):
    def __init__(self, connector: asyncpg.pool.Pool):
        super().__init__()
        self.connector = connector

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        async with self.connector.acquire() as connect:
            data['request'] = Request(connect)
            return await handler(event, data)
    



