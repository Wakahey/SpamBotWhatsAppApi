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
from .schemas import CreateSeller, UpdateSeller, PartialSeller, SellerSocial


async def create_seller(session: AsyncSession, seller_in: SellerSocial) -> WholesaleCustomer:
    seller_data = seller_in.model_dump()
    social_network_data = seller_data.pop("social_network", None)

    seller = WholesaleCustomer(**seller_data)

    if social_network_data:
        social_network = SocialNetwork(**social_network_data)
        seller.social_network = social_network

    session.add(seller)
    print(seller.social_network.telegram_url)
    await session.commit()
    return seller


async def get_sellers(session: AsyncSession) -> list[WholesaleCustomer]:
    stmt = select(WholesaleCustomer).order_by(WholesaleCustomer.id)
    result = await session.execute(stmt)
    seller = result.scalars().all()
    return list(seller)


async def get_sellers_where(session: AsyncSession, customer_type: WholesaleCustomer.customer_type) -> list[
    WholesaleCustomer]:
    stmt = select(WholesaleCustomer).where(WholesaleCustomer.customer_type == customer_type).order_by(
        WholesaleCustomer.id)
    result = await session.execute(stmt)
    seller = result.scalars().all()
    return list(seller)


async def get_seller(session: AsyncSession,
                     seller_id: int) -> WholesaleCustomer | None:
    return await session.get(WholesaleCustomer, seller_id)


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
