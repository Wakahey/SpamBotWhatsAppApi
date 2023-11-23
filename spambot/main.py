from fastapi import FastAPI
import uvicorn
from seller.views import router as seller_router
from contextlib import asynccontextmanager
from core.models.db_helper import db_helper
from core.models.seller import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan)
app.include_router(seller_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
