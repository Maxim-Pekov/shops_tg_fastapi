import datetime
from http.client import HTTPException

from slugify import slugify
from app.backend.db import Base, SessionLocal
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float, DateTime
from sqlalchemy.orm import relationship, Session


from app.models.product_store import ProductStore
from app.models.store import Store
from app.schemas import CreateProduct
from fastapi import status


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
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
        store = db.query(Store).filter_by(name=create_product.store_name).one()
        product = Product(name=create_product.name,
                          description=create_product.description,
                          image_url=create_product.image_url,
                          category_id=create_product.category,
                          rating=0.0,
                          slug=slugify(create_product.name))

        db.add(product)
        db.commit()
        product_store = ProductStore(product_id=product.id,
                                     store_id=store.id,
                                     price=create_product.price)
        db.add(product_store)
        db.commit()
        return {
            'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'
        }

    @staticmethod
    def get_products_by_category(db: Session, category_slug: str):
        from app.models import Category
        category = db.query(Category).filter_by(slug=category_slug).one()
        subcategories = db.query(Category).filter_by(parent_id=category.id)
        categories_and_subcategories = [category.id] + [i.id for i in subcategories.all()]
        products_category = db.query(Product).where(
            Product.category_id.in_(categories_and_subcategories), Product.is_active == True
        )
        return products_category.all()

    @staticmethod
    def create_or_update_product(db: Session, create_product: CreateProduct):
        product_slug = slugify(create_product.name)
        store = db.query(Store).filter_by(name=create_product.store_name).one()
        product = db.query(Product).filter_by(slug=slugify(create_product.name)).first()
        if product:
            product.name = create_product.name
            product.description = create_product.description
            product.image_url = create_product.image_url
            product.category_id = create_product.category
            product.rating = product.rating
            product.slug = product_slug
        else:
            product = Product(
                name=create_product.name,
                description=create_product.description,
                image_url=create_product.image_url,
                category_id=create_product.category,
                rating=0.0,
                slug=product_slug
            )
            db.add(product)
            db.commit()
        product_store = (
            db.query(ProductStore).filter_by(product_id=product.id, store_id=store.id).first()
        )

        if product_store:
            product_store.price = create_product.price
        else:
            product_store = ProductStore(
                product_id=product.id,
                store_id=store.id,
                price=create_product.price
            )
            db.add(product_store)
        db.commit()
        db.refresh(product)

        return product

    @staticmethod
    def get_all_product_by_name(product: str):
        """
        Метод получает все продукты из БД у которых есть частичное совпадение с переданным словом.
        """
        if not product:
            return []
        import re
        db = SessionLocal()
        escaped_word = slugify(product)
        re.sub(r'[^a-zA-Z0-9 ]', '', product)
        pattern = f'%{escaped_word}%'
        products = db.query(Product).filter(Product.slug.ilike(pattern)).all()
        return products
