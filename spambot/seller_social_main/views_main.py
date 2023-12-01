from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from spambot.core.config import templates
from spambot.core.models.db_helper import db_helper
from spambot.seller import crud
from fastapi.responses import HTMLResponse

route = APIRouter(prefix="", tags=["Sellers main view"])


@route.get("/", response_class=HTMLResponse)
async def test_all(
        request: Request,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    result = await crud.get_sellers(session=session)
    return templates.TemplateResponse("test_all_sellers.html", context={"request": request,
                                                                        "data": result})


@route.get("/test_add/", response_class=HTMLResponse)
async def test_add(
        request: Request,
):
    return templates.TemplateResponse("test_create_seller.html", context={"request": request})


@route.get("/razborka/", response_class=HTMLResponse)
async def test_razborka(
        request: Request,
):
    application_type = "Разборка"
    return templates.TemplateResponse("test_by_razborka.html", context={"request": request,
                                                                        "application_type": application_type})


@route.get("/applications/", response_class=HTMLResponse)
async def applications_sending(
        request: Request,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    data = await crud.get_applications(session=session)

    return templates.TemplateResponse("applications_sender.html", context={"request": request,
                                                                           "data": data})

# @route.get("/view/{customer_type}/", response_class=HTMLResponse)
# async def get_sellers_customer_type(
#         request: Request,
#         customer_type: str = "all",
#         session: AsyncSession = Depends(db_helper.scoped_session_dependency)
# ):
#     if customer_type == "all":
#         result = await crud.get_sellers(session=session)
#     else:
#         result = await crud.get_sellers_where(session=session, customer_type=customer_type)
#     return templates.TemplateResponse("all_get_sellers.html", context={"request": request,
#                                                                        "data": result,
#                                                                        "customer_type": customer_type})


# @route.get("/bot_sending/", response_class=HTMLResponse)
# async def bot_sending_form(request: Request,
#                            session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
#     return templates.TemplateResponse("bot_sending.html", context={"request": request})
