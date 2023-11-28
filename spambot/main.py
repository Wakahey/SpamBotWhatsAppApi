from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
import uvicorn
from seller.views import router as seller_router
from contextlib import asynccontextmanager
from core.models.db_helper import db_helper
from core.models.seller import Base
from spambot.seller_social_main.views_main import route as views_main
from spambot.Sending_bots.send_view import router as sending_route


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan)
app.include_router(seller_router)
app.include_router(views_main)
app.include_router(sending_route)


@app.middleware("http_redirect")
async def redirect_to_home(request, call_next):
    try:
        return await call_next(request)
    except HTTPException as exc:
        redirect_url = '/view/all'
        if exc.status_code == 404:
            return RedirectResponse(url=redirect_url)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
