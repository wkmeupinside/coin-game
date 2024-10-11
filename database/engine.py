from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

engine = create_async_engine(url="sqlite+aiosqlite:///database.db")

SessionLocal = async_sessionmaker(engine)
