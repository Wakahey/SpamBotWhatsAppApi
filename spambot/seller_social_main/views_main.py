from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from spambot.core.config import templates
from spambot.core.models.db_helper import db_helper
from spambot.seller import crud
from spambot.seller.schemas import SellerView
from fastapi.responses import HTMLResponse
from spambot.core.models.seller import WholesaleCustomer
from spambot.seller.schemas import BaseSeller
from fastapi.responses import RedirectResponse

route = APIRouter(prefix="", tags=["Sellers main view"])


@route.get("/create/", response_class=HTMLResponse)
async def get_create_form(request: Request):
    return templates.TemplateResponse("create_form.html", context={"request": request})


@route.get("/view/{customer_type}/", response_class=HTMLResponse)
async def get_sellers_customer_type(
        request: Request,
        customer_type: str = "all",
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    if customer_type == "all":
        result = await crud.get_sellers(session=session)
    else:
        result = await crud.get_sellers_where(session=session, customer_type=customer_type)
    return templates.TemplateResponse("all_get_sellers.html", context={"request": request,
                                                                       "data": result,
                                                                       "customer_type": customer_type})


@route.get("/bot_sending/", response_class=HTMLResponse)
async def bot_sending_form(request: Request,
                           session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return templates.TemplateResponse("bot_sending.html", context={"request": request})
