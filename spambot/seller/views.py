from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from spambot.example_templates.schemas import SellerView, BaseSeller
from . import crud
from spambot.core.models.db_helper import db_helper
from spambot.Sending_bots.schemas import InputSendingInfo
from spambot.Sending_bots.whatsapp_sending.whatsapp_sender import start_sending

router = APIRouter(prefix="/request", tags=["Send request"])


@router.post("/create/", response_model=SellerView)
async def create_seller(
        seller_in: BaseSeller,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.create_seller(session=session, seller_in=seller_in)


@router.post("/used_parts/")
async def input_info(
        info: InputSendingInfo,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    sellers = crud.get_sellers_where(session=session, type_part=info.application_type,
                                     specialization=info.motorcycle_brand)
    start_sending(data=info, sellers=sellers)

    result = await crud.create_applications(session=session, application_info=info)

    # raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ошибка в данных")
#
#
# @router.get("/", response_model=list[SellerView])
# async def get_sellers(
#         session: AsyncSession = Depends(db_helper.scoped_session_dependency)
# ):
#     return await crud.get_sellers(session=session)
#
#
# @router.get("/{seller_id}", response_model=SellerView)
# async def get_seller(seller: Seller = Depends(get_seller_by_id)):
#     return seller

# @router.delete("/{seller_id}")
# async def delete_sellers(seller: Seller = Depends(get_seller_by_id),
#                          session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
#     return await crud.delete_seller(seller=seller, session=session)


# @router.put("/{seller_id}")
# async def update_sellers(seller_update: PartialSeller,
#                          seller: Seller = Depends(get_seller_by_id),
#                          session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
#     return await crud.update_seller_partial(seller=seller,
#                                             session=session,
#                                             seller_update=seller_update)
