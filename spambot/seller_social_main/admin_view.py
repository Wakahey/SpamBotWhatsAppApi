# -*- coding: utf-8 -*-
from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from spambot.core.models.db_helper import db_helper
from spambot.seller import crud
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from spambot.templates.admin.admin_templates_path import folder_path

route = APIRouter(prefix="/admin", tags=["Sellers main view"])

templates = Jinja2Templates(directory=folder_path)


@route.get("/", response_class=HTMLResponse)
async def admin_view(
        request: Request,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    result = await crud.get_sellers(session=session)
    return templates.TemplateResponse("all_sellers_table_admin.html", context={"request": request,
                                                                               "data": result})


@route.get("/add/user/", response_class=HTMLResponse)
async def add_user(
        request: Request,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    moto_brand = await crud.get_moto_brand(session=session)
    return templates.TemplateResponse("create_seller.html", context={"request": request,
                                                                     "model_moto": moto_brand})


@route.get("/add/moto/", response_class=HTMLResponse)
async def add_moto(
        request: Request,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    moto_brand = await crud.get_moto_brand(session=session)
    return templates.TemplateResponse("add_moto_brand.html", context={"request": request,
                                                                      "model_moto": moto_brand})
