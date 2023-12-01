"""
Create
Read
Update
Delete
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from spambot.example_templates.schemas import BaseSeller
from spambot.core.models.seller import WholesaleCustomer, Applications
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

# async def update_seller_partial(session: AsyncSession,
#                                 seller: WholesaleCustomer,
#                                 seller_update: PartialSeller,
#                                 partial: bool = True) -> WholesaleCustomer:
#     for key, value in seller_update.model_dump(exclude_unset=partial).items():
#         setattr(seller, key, value)
#     await session.commit()
#     return seller

# async def delete_seller(session: AsyncSession,
#                         seller: WholesaleCustomer) -> str:
#     # smt = delete(WholesaleCustomer).where(WholesaleCustomer.id == seller_id)
#     # await session.execute(smt)
#     await session.delete(seller)
#     await session.commit()
#     return f"Delete {seller.name_organization} complete"
