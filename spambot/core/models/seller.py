from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class WholesaleCustomer(Base):
    __tablename__ = "customer"

    id = Column(Integer, primary_key=True)
    name_organization = Column(String, nullable=False)
    type_part = Column(String, nullable=False)
    specialization = Column(String, default="запчасти", nullable=False)
    location = Column(String, default=None)
    whatsapp = Column(Integer, default=None)
    vk_id = Column(Integer, default=None)
    email = Column(String, default=None)
    date_add = Column(DateTime, default=datetime.now)

    applications = relationship("Association", back_populates="customer")


class Applications(Base):
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True)
    motorcycle_brand = Column(String, nullable=False)
    motorcycle_model = Column(String, nullable=False)
    manufacturing_year = Column(String)
    vin_number = Column(String)
    part_name_or_article = Column(String)
    social_network = Column(String)
    additional_info = Column(String)
    application_type = Column(String)
    datetime_create = Column(String, default=datetime.now())

    sellers = relationship("Association", back_populates="application", cascade="all, delete-orphan")


class Association(Base):
    __tablename__ = "association"
    applications_id = Column(Integer, ForeignKey("applications.id"), primary_key=True)
    customer_id = Column(Integer, ForeignKey("customer.id"), primary_key=True)

    application = relationship("Applications", back_populates="sellers", lazy="joined")
    customer = relationship("WholesaleCustomer", back_populates="applications", lazy="joined", passive_deletes=True)


class BrandMoto(Base):
    __tablename__ = "brand_moto"
    id = Column(Integer, primary_key=True)
    name = Column(String, primary_key=True, nullable=False)

    models = relationship("ModelMoto", back_populates="brand")


class ModelMoto(Base):
    __tablename__ = "model_moto"
    id = Column(Integer, primary_key=True)
    brand_id = Column(Integer, ForeignKey("brand_moto.id"), nullable=False)
    model_moto = Column(String, nullable=False)

    brand = relationship("BrandMoto", back_populates="models")
