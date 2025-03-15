from sqlalchemy import Column, Integer, String, Boolean
from slugify import slugify
from sqlalchemy.orm import relationship
from sqlalchemy.orm import relationship, Session
from app.backend.db import Base
from app.schemas import CreateStore


class Store(Base):
    __tablename__ = 'stores'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    slug = Column(String, unique=True, index=True)

    products = relationship('ProductStore', back_populates='store')

    @staticmethod
    def get_all_stories(db: Session):
        return db.query(Store).all()

    @staticmethod
    def create_store(db: Session, create_store: CreateStore):
        store = Store(name=create_store.name,
                      address=create_store.address,
                      slug=slugify(create_store.name))
        db.add(store)
        db.commit()
        return db.query(Store).all()