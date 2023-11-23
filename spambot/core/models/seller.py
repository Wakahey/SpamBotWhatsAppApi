from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class WholesaleCustomer(Base):
    __tablename__ = "customer"

    id = Column(Integer, primary_key=True)
    name_organization = Column(String, nullable=False)
    location = Column(String, default=None)
    associative_words = Column(String, default="запчасти")
    date_add = Column(DateTime, default=datetime.now)

    social_network = relationship(
        "SocialNetwork", backref="customer", cascade="all", lazy="select"
    )


class SocialNetwork(Base):
    __tablename__ = "social_network"

    customer_id = Column(
        Integer, ForeignKey("customer.id"), primary_key=True, nullable=False
    )
    type_order = Column(String)
    telegram_url = Column(String, default=None)
    vk_url = Column(String, default=None)
    email = Column(String, default=None)
    phone_number = Column(String, default=None)
