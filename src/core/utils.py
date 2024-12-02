from fastapi                import FastAPI, UploadFile
from contextlib             import asynccontextmanager
from dotenv                 import load_dotenv

from src.database.base      import Base
from src.database.db_helper import db_helper

import os
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

def check_picked_file(file: UploadFile) -> bool:
    if file.filename and str(file.content_type).startswith("image/"):
        return True
    else:
        return False

def remove_image(title: str) -> None:
    try:
        os.remove("static/" + title)
        logging.warning("IMAGE REMOVED")
    except:
        logging.warning("IMAGE NOT FOUND")

def add_image(file: UploadFile) -> str:
    try:
        timestamp   = get_timestamp()                   # 1706520261
        format      = str(file.filename).split('.')[-1] # jpg/jpeg/png
        unique_name = f"{timestamp}.{format}"           # 1706520261.png
        file_name   = os.path.join("static", unique_name)
        with open(file_name, "wb") as image_file:
            image_file.write(file.file.read())
        return unique_name
    except Exception as e:
        logging.warning(e)
        return ""
