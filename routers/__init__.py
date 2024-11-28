from fastapi                import APIRouter, HTTPException, Depends
from sqlalchemy             import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.db_helper     import db_helper
from database.base          import User, Test, Category, Product, Order
from core.schemas           import *
from core.utils             import *