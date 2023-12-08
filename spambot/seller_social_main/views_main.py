# -*- coding: utf-8 -*-
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
    return templates.TemplateResponse("all_sellers_table.html", context={"request": request,
                                                                         "data": result})


@route.get("/spambot/razborka", response_class=HTMLResponse)
async def test_razborka(
        request: Request,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    brand_moto = await crud.get_moto_brand(session=session)
    name = "Форма рассылки по б/у разборкам"
    application_type = "Разборка"
    return templates.TemplateResponse("sending_form.html", context={"request": request,
                                                                    "model_moto": brand_moto,
                                                                    "name": name,
                                                                    "application_type": application_type})


@route.get("/spambot/new/original", response_class=HTMLResponse)
async def new_original(
        request: Request,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    brand_moto = await crud.get_moto_brand(session=session)
    name = "Новые оригинальные запчасти"
    application_type = "Новые оригинальные"
    return templates.TemplateResponse("sending_form.html", context={"request": request,
                                                                    "model_moto": brand_moto,
                                                                    "name": name,
                                                                    "application_type": application_type})


@route.get("/spambot/new/no_orinal", response_class=HTMLResponse)
async def new_no_original(
        request: Request,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    brand_moto = await crud.get_moto_brand(session=session)
    name = "Новые НЕ оригинальные запчасти"
    application_type = "Новые не оригинальные"
    return templates.TemplateResponse("sending_form.html", context={"request": request,
                                                                    "model_moto": brand_moto,
                                                                    "name": name,
                                                                    "application_type": application_type})


@route.get("/spambot/tires", response_class=HTMLResponse)
async def tires(
        request: Request,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    brand_moto = await crud.get_moto_brand(session=session)
    name = "Поставщики резины"
    application_type = "Резина"
    return templates.TemplateResponse("sending_form.html", context={"request": request,
                                                                    "model_moto": brand_moto,
                                                                    "name": name,
                                                                    "application_type": application_type})


@route.get("/applications/", response_class=HTMLResponse)
async def applications_sending(
        request: Request,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    data = await crud.get_applications(session=session)

    return templates.TemplateResponse("all_applications.html", context={"request": request,
                                                                        "data": data})


@route.get("/image/", response_class=HTMLResponse)
async def get_image_view(
        request: Request,
):
    return templates.TemplateResponse("get_image_screenshot.html", context={"request": request})
