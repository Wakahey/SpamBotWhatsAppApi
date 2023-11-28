from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import time
from .schemas import Seller, CreateSeller, SellerView, PartialSeller, SellerSocial, SellerSocialResponse
from . import crud
from spambot.core.models.db_helper import db_helper, get_seller_by_id

router = APIRouter(prefix="/request", tags=["Send request"])


@router.post("/create/", response_model=SellerSocialResponse)
async def create_seller(
        seller_in: SellerSocial,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    print(seller_in.social_network.telegram_url)
    return await crud.create_seller(session=session, seller_in=seller_in)


@router.get("/", response_model=list[SellerView])
async def get_sellers(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.get_sellers(session=session)


@router.get("/{seller_id}", response_model=SellerView)
async def get_seller(seller: Seller = Depends(get_seller_by_id)):
    return seller


@router.delete("/{seller_id}")
async def delete_sellers(seller: Seller = Depends(get_seller_by_id),
                         session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await crud.delete_seller(seller=seller, session=session)


@router.put("/{seller_id}")
async def update_sellers(seller_update: PartialSeller,
                         seller: Seller = Depends(get_seller_by_id),
                         session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await crud.update_seller_partial(seller=seller,
                                            session=session,
                                            seller_update=seller_update)
