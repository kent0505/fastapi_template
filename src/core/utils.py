from fastapi                import FastAPI
from contextlib             import asynccontextmanager
from dotenv                 import load_dotenv
from aiogram                import Bot, Dispatcher

from src.database.base      import Base
from src.database.db_helper import db_helper
from src.bot.handlers       import router

import time, logging, asyncio, os

bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()

async def start_bot():
    dp.include_router(router)
    logging.info("Starting Telegram bot")
    try:
        await dp.start_polling(bot)
    except asyncio.CancelledError:
        logging.info("Telegram bot stopped")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    load_dotenv()
    logging.info("STARTUP")
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    bot_task = asyncio.create_task(start_bot())
    yield
    # shutdown
    logging.info("SHUTDOWN")
    bot_task.cancel()
    await db_helper.dispose()

def get_timestamp() -> int:
    timestamp: int = int(time.time())
    return timestamp
