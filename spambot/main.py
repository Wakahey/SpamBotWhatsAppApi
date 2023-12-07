from fastapi import FastAPI
import uvicorn
from seller.views import router as seller_router
from contextlib import asynccontextmanager
from core.models.db_helper import db_helper
from core.models.seller import Base
from spambot.seller_social_main.views_main import route as views_main


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan)
app.include_router(seller_router)
app.include_router(views_main)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
