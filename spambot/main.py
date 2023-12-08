from fastapi import FastAPI
import uvicorn
from spambot.seller.views import router as seller_router
from contextlib import asynccontextmanager
from spambot.core.models.db_helper import db_helper
from spambot.core.models.seller import Base
from spambot.seller_social_main.views_main import route as views_main
from spambot.seller_social_main.admin_view import route as admin_view_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan)
app.include_router(seller_router)
app.include_router(views_main)
app.include_router(admin_view_router)
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
