import datetime

from app.backend.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float, DateTime
from sqlalchemy.orm import relationship
from app.models.category import *
from app.models.product_store import ProductStore
from app.models.store import Store
from app.schemas import CreateProduct
from fastapi import status


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    slug = Column(String, unique=True, index=True)
    description = Column(String)
    image_url = Column(String)
    category_id = Column(Integer, ForeignKey('categories.id'))
    supplier_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    rating = Column(Float)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    category = relationship('Category', back_populates='products')
    stores = relationship('ProductStore', back_populates='product')

    @staticmethod
    def get_all_products(db: Session):
        return db.query(Product).all()

    @staticmethod
    def create_product(db: Session, create_product: CreateProduct):
        store = db.query(Store).filter_by(name=create_product.store_name)
        product = Product(name=create_product.name,
                          description=create_product.description,
                          price=create_product.price,
                          image_url=create_product.image_url,
                          stock=create_product.stock,
                          category_id=create_product.category,
                          store_id=create_product.store,
                          rating=0.0,
                          slug=slugify(create_product.name))
        product_store = ProductStore(product_id=product.id,
                                     store_id=store.id,
                                     price=create_product.price)
        db.add(product)
        db.commit()
        return {
            'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'
        }