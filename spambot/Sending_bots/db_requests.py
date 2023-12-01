from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from spambot.core.models.seller import WholesaleCustomer
from spambot.seller import crud

# async def sending_get_sellers_where(session: AsyncSession,
#                                     seller_type,
#                                     sending_type
#                                     ) -> list[WholesaleCustomer]:
#     if sending_type == "all":
#         result = await crud.get_sellers(session=session)
#         return result
#     else:
#         stmt = (
#             select(WholesaleCustomer)
#             .join(SocialNetwork, WholesaleCustomer.id == SocialNetwork.customer_id)
#             .where(
#                 (WholesaleCustomer.customer_type == seller_type) &
#                 (func.length(SocialNetwork.__dict__[sending_type]) > 3)
#             )
#         )
#
#         result = await session.execute(stmt)
#         sellers = result.scalars().all()
#         return list(sellers)
