from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Any, Awaitable, Callable, Dict


class TestMiddleware(BaseMiddleware):
    async def __call__(
        self, 
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], 
        event: TelegramObject, 
        data: Dict[str, Any]
    ) -> Any:
        # действия до обработчика 
        print("AAA")
        result = await handler(event, data)
        # действия после обработчика 
        print("BBB")
        return result
