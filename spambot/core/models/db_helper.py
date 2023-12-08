from typing import Annotated

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
    AsyncSession
)
from sqlalchemy.orm import sessionmaker
from asyncio import current_task
from fastapi import Path, Depends, HTTPException, status
from spambot.core.config import setting
from spambot.seller import crud
from spambot.core.models.seller import WholesaleCustomer


class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task
        )
        return session

    async def scoped_session_dependency(self) -> AsyncSession:
        session = self.get_scoped_session()
        yield session
        await session.close()


db_helper = DatabaseHelper(url=setting.db_url, echo=setting.db_echo)


async def get_seller_by_id(seller_id: Annotated[int, Path],
                           session: AsyncSession =
                           Depends(db_helper.scoped_session_dependency)) \
        -> WholesaleCustomer:
    seller = await crud.get_seller(session=session, seller_id=seller_id)
    if seller is not None:
        return seller

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Seller {seller_id} not found"
    )
