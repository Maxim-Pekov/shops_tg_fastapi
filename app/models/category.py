from slugify import slugify
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, insert
from sqlalchemy.orm import relationship, Session
from app.models.products import Product
from app.backend.db import Base
from app.schemas import CreateCategory


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    slug = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    parent_id = Column(Integer, ForeignKey('categories.id'), nullable=True)

    products = relationship("Product", back_populates="category")

    @staticmethod
    def get_all_categories(db: Session):
        return db.query(Category).all()

    @staticmethod
    def create_categories(db: Session, create_category: CreateCategory):
        category = Category(name=create_category.name,
                            parent_id=create_category.parent_id,
                            slug=slugify(create_category.name))
        db.add(category)
        db.commit()
        return db.query(Category).all()
