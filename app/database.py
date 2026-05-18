from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
import config

SQLALCHEMY_DATABASE_URL = config.DATABASE_URL

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

AsyncSession = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with AsyncSession() as db:
        yield db