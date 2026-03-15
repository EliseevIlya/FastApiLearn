from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.core.config import get_db_url

engine = create_async_engine(
    get_db_url(),
    echo=True
)

async_session = async_sessionmaker(
    engine,
    expire_on_commit=False
)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
