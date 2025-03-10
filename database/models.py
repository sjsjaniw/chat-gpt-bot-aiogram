from datetime import datetime, timezone
from sqlalchemy import ForeignKey, Integer, BigInteger, String, Boolean, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from dotenv import load_dotenv
import os

load_dotenv()
# engine = create_async_engine(os.getenv("DATABASE_URL"))
engine = create_async_engine(url = 'sqlite+aiosqlite:///db.sqlite3')

async_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

class UserOrm(Base):
    __tablename__ = "users"
    id = mapped_column(Integer, primary_key=True)
    tg_id = mapped_column(BigInteger, nullable=False, unique=True)
    language = mapped_column(String(2), nullable=False, default="ru")
    ai_id = mapped_column(Integer, nullable=False, default=0)
    is_admin = mapped_column(Boolean, nullable=False, default=False)
    
    ai = relationship("AiUserOrm")

class AiUserOrm(Base):
    __tablename__ = "ai_of_users"
    id = mapped_column(Integer, primary_key=True)
    tg_id = mapped_column(BigInteger, ForeignKey("users.tg_id"))
    level = mapped_column(Integer, nullable=False, default=0)

    gpt4omini = mapped_column(Integer, nullable=False, default=20)
    gpt4o = mapped_column(Integer, nullable=False, default=0)
    llama31405b = mapped_column(Integer, nullable=False, default=0)
    claude35sonnet = mapped_column(Integer, nullable=False, default=0)
    playgroundv25 = mapped_column(Integer, nullable=False, default=1)
    sd3 = mapped_column(Integer, nullable=False, default=3)

    date_of_issued_requests = mapped_column(DateTime, nullable=True, default=datetime.now(timezone.utc).replace(tzinfo=None))
    date_of_subscription = mapped_column(DateTime, nullable=True) 

async def async_db_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)