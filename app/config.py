from advanced_alchemy.extensions.litestar import SQLAlchemyAsyncConfig, SQLAlchemyInitPlugin
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from typing import AsyncGenerator
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
  raise ValueError("DATABASE_URL environment variable is not set.")

engine = create_async_engine(DATABASE_URL, echo=True)
session_maker = async_sessionmaker(engine, expire_on_commit=False)
config = SQLAlchemyAsyncConfig(connection_string=DATABASE_URL, session_maker=session_maker)
alchemy = SQLAlchemyInitPlugin(config=config)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
  if config.session_maker is None:
    raise ValueError("Session maker is not initialized.")
  async with config.session_maker() as session:
    yield session
