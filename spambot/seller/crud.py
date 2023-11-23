"""
Create
Read
Update
Delete
"""

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result

from spambot.core.models.seller import WholesaleCustomer, SocialNetwork
from .schemas import CreateSeller, UpdateSeller, PartialSeller


async def create_seller(session: AsyncSession,
                        seller_in: CreateSeller) -> WholesaleCustomer:
    seller = WholesaleCustomer(**seller_in.model_dump())
    session.add(seller)
    await session.commit()
    # await session.refresh(seller)
    return seller


async def get_sellers(session: AsyncSession) -> list[WholesaleCustomer]:
    stmt = select(WholesaleCustomer).order_by(WholesaleCustomer.id)
    result = await session.execute(stmt)
    seller = result.scalars().all()
    return list(seller)


async def get_seller(session: AsyncSession,
                     seller_id: int) -> WholesaleCustomer | None:
    return await session.get(WholesaleCustomer, seller_id)


# async def update_seller(session: AsyncSession,
#                         seller: WholesaleCustomer,
#                         seller_update: UpdateSeller) -> WholesaleCustomer:
#     for key, value in seller_update.model_dump().items():
#         setattr(seller, key, value)
#     await session.commit()
#     return seller


async def update_seller_partial(session: AsyncSession,
                                seller: WholesaleCustomer,
                                seller_update: PartialSeller,
                                partial: bool = True) -> WholesaleCustomer:
    for key, value in seller_update.model_dump(exclude_unset=partial).items():
        setattr(seller, key, value)
    await session.commit()
    return seller


async def delete_seller(session: AsyncSession,
                        seller: WholesaleCustomer) -> str:
    # smt = delete(WholesaleCustomer).where(WholesaleCustomer.id == seller_id)
    # await session.execute(smt)
    await session.delete(seller)
    await session.commit()
    return f"Delete {seller.name_organization} complete"
