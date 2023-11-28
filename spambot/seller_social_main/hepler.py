from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result

from spambot.core.models.seller import WholesaleCustomer, SocialNetwork
from spambot.seller.schemas import CreateSeller
