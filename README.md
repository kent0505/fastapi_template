### Run
1) create .env file and add this
```
KEY=yoursecretjwtkey
USERNAME=adminusername
PASSWORD=adminpassword
```
2) virtualenv venv
3) venv\Scripts\activate or source venv/bin/activate
4) pip install -r requirements.txt
5) uvicorn src.main:app --reload
### Alembic
1) alembic init -t async migrations
2) migrations/env.py
```
from database.base import *
```
3) migrations/env.py
```
target_metadata = Base.metadata
```
4) alembic.ini
```
sqlalchemy.url = sqlite+aiosqlite:///sqlite.db
```
5) alembic revision --autogenerate -m "init"
6) alembic upgrade head
7) alembic stamp head
### Others
```
sudo lsof -t -i tcp:8000 | xargs kill -9
```
Команда запуска на timeweb ```uvicorn src.main:app --host 0.0.0.0 --port 8000```