import datetime

from sqlalchemy import Column, ForeignKey, Integer, Float, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from app.backend.db import Base


class ProductStore(Base):
    __tablename__ = 'product_store'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    store_id = Column(Integer, ForeignKey('stores.id'), nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=True)

    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    product = relationship('Product', back_populates='stores')
    store = relationship('Store', back_populates='products')
