from fastapi            import FastAPI
from contextlib         import asynccontextmanager
from dotenv             import load_dotenv
from database.base      import Base
from database.db_helper import db_helper
import time
import logging

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    load_dotenv()
    # logging.basicConfig(
    #     filename = "logfile.log",
    #     level    = logging.INFO,
    #     format   = "%(asctime)s - %(levelname)s - %(message)s",
    #     datefmt  = "%d-%m-%Y %H:%M:%S" # 29-01-2024 14:19:28,
    # )
    logging.info("STARTUP")
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # shutdown
    logging.info("SHUTDOWN")
    await db_helper.dispose()

def get_timestamp() -> int:
    timestamp: int = int(time.time())
    return timestamp
