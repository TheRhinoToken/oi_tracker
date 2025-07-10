# backend/database.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, Float, DateTime
from datetime import datetime

DATABASE_URL = "sqlite+aiosqlite:///./option_data.db"

engine = create_async_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

class OptionData(Base):
    __tablename__ = "option_data"

    id = Column(Integer, primary_key=True, index=True)
    strike_price = Column(Float, index=True)
    call_oi = Column(Integer)
    call_oi_change = Column(Integer)
    call_volume = Column(Integer)
    put_oi = Column(Integer)
    put_oi_change = Column(Integer)
    put_volume = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
