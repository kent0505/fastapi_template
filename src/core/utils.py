from fastapi                import FastAPI, UploadFile
from contextlib             import asynccontextmanager
from dotenv                 import load_dotenv
from datetime               import datetime, timedelta

from src.database.base      import Base
from src.database.db_helper import db_helper

import re, os, time, logging

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

def get_yesterday() -> str:
    date = datetime.now() - timedelta(days=1.5)
    return date.strftime("%Y%m%d")

def extract_id(text) -> str:
    match = re.search(r"/id/(\d+)", text)
    if (match):
        return f"https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/{match.group(1)}.png&w=100&h=100&scale=crop&cquality=100&location=origin"
    return ""

def extract_game_id(url: str) -> int | None:
    match = re.search(r"/gameId/(\d+)", url)
    return int(match.group(1)) if match else None

def get_coordinates(transform: str) -> str:
    return transform.replace("transform:translate(", "").replace("px", "").replace(")", "").replace(", ", "x")

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
