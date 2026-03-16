from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import auth_router
from app.core.loguru_config import setup_logging
from app.db.database import engine
from app.db.redis import redis_client_init
from loguru import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- STARTUP ---
    setup_logging()

    await redis_client_init.connect()

    async with engine.begin() as conn:
        pass

    logger.info("All resources are connected")
    try:
        yield
    finally:
        # --- SHUTDOWN ---
        logger.info("Closing all resources...")
        await redis_client_init.close()
        await engine.dispose()
        logger.info("All resources are closed")


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)


@app.get("/health")
async def root():
    return {"message": "Hello World"}

