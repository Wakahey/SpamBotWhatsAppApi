"""
Create
Read
Update
Delete
"""

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from spambot.core.models.schemas import BaseSeller
from spambot.core.models.seller import (WholesaleCustomer,
                                        Applications,
                                        Association, ModelMoto, BrandMoto)
from spambot.Sending_bots.schemas import InputSendingInfo


async def create_seller(session: AsyncSession, seller_in: BaseSeller) -> WholesaleCustomer:
    seller_data = seller_in.model_dump()
    seller = WholesaleCustomer(**seller_data)

    session.add(seller)
    await session.commit()
    return seller


async def get_sellers(session: AsyncSession) -> list[WholesaleCustomer]:
    stmt = select(WholesaleCustomer).order_by(WholesaleCustomer.id)
    result = await session.execute(stmt)
    seller = result.scalars().all()
    return list(seller)


async def get_applications(session: AsyncSession) -> list[Applications]:
    stmt = select(Applications).order_by(Applications.id)
    result = await session.execute(stmt)
    seller = result.scalars().all()
    return list(seller)


async def create_applications(application_info: InputSendingInfo, session: AsyncSession):
    application_data = application_info.model_dump()
    application_object = Applications(**application_data)
    session.add(application_object)
    await session.commit()
    return application_object


async def delete_application(session: AsyncSession,
                             application_id: int) -> str:
    smt = select(Applications).where(Applications.id == application_id)
    result = await session.execute(smt)
    application = result.scalar()
    await session.delete(application)
    await session.commit()


async def delete_seller(session: AsyncSession,
                        seller_id: int) -> str:
    smt = select(WholesaleCustomer).where(WholesaleCustomer.id == seller_id)
    result = await session.execute(smt)
    seller = result.scalar()
    await session.delete(seller)
    await session.commit()


async def create_association(application: Applications,
                             seller_li: list[WholesaleCustomer],
                             session: AsyncSession):
    data = []
    for seller in seller_li:
        data.append({'applications_id': application.id,
                     'customer_id': seller.id,
                     'phone_number': seller.whatsapp
                     })
    stmt = insert(Association).values(data)
    await session.execute(stmt)
    await session.commit()


async def get_association(application_id: int,
                          session: AsyncSession) -> list[Association]:
    stmt = select(Association).where(Association.applications_id == application_id)
    result = await session.execute(stmt)
    association_all = result.scalars().all()
    return list(association_all)


async def get_moto_brand(session: AsyncSession) -> list[ModelMoto]:
    stmt = select(BrandMoto)
    result = await session.execute(stmt)
    brand_moto = result.scalars().all()
    return list(brand_moto)


async def get_moto_model(session: AsyncSession, brand: str):
    stmt = (select(BrandMoto)
            .options(joinedload(BrandMoto.models))
            .where(BrandMoto.name == brand))
    result = await session.execute(stmt)
    brand_model = result.scalar()
    if brand_model is not None:
        models = [model.model_moto for model in brand_model.models]
        return {"models": models}
    else:
        return {"error": "Моделей у мотоцикла нет"}


async def get_sellers_where(session: AsyncSession,
                            type_part: WholesaleCustomer.type_part,
                            specialization: WholesaleCustomer.specialization) \
        -> list[WholesaleCustomer]:
    stmt = (select(WholesaleCustomer)
            .where(WholesaleCustomer.type_part == type_part)
            .where(WholesaleCustomer.specialization == specialization)
            .order_by(WholesaleCustomer.id))
    result = await session.execute(stmt)
    seller = result.scalars().all()
    return list(seller)


async def get_seller(session: AsyncSession,
                     seller_id: int) -> WholesaleCustomer | None:
    return await session.get(WholesaleCustomer, seller_id)
