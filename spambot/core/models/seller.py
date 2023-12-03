from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table
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

    applications = relationship("Association", back_populates="customer")


class Applications(Base):
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True)
    motorcycle_brand = Column(String, nullable=False)
    motorcycle_model = Column(String, nullable=False)
    part_name_or_article = Column(String)
    additional_info = Column(String)
    application_type = Column(String)
    datetime_create = Column(String, default=datetime.now())
    sellers = relationship("Association", back_populates="application", cascade="all, delete-orphan")


class Association(Base):
    __tablename__ = "association"
    applications_id = Column(Integer, ForeignKey("applications.id"), primary_key=True)
    customer_id = Column(Integer, ForeignKey("customer.id"), primary_key=True)
    phone_number = Column(String)

    application = relationship("Applications", back_populates="sellers", lazy="joined")
    customer = relationship("WholesaleCustomer", back_populates="applications", lazy="joined", passive_deletes=True)


class ModelMoto(Base):
    __tablename__ = "model_moto"
    id = Column(Integer, primary_key=True)
    model_moto = Column(String, primary_key=True)
