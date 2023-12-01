from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship, Mapped
from datetime import datetime

Base = declarative_base()


class WholesaleCustomer(Base):
    __tablename__ = "customer"

    id = Column(Integer, primary_key=True)
    name_organization = Column(String, nullable=False)
    type_part = Column(String, nullable=False)
    specialization = Column(String, default="запчасти")
    location = Column(String, default=None)
    whatsapp = Column(Integer, default=None)
    email = Column(String, default=None)
    date_add = Column(DateTime, default=datetime.now)


class Applications(Base):
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True)
    motorcycle_brand = Column(String, nullable=False)
    motorcycle_model = Column(String, nullable=False)
    part_name_or_article = Column(String)
    additional_info = Column(String)
    application_type = Column(String)
