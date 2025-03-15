from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = create_engine('sqlite:///:memory:')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Products(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)
    description = Column(String)

    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"))


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    product = relationship("Products", backref="category", cascade="all, delete")


Base.metadata.drop_all(engine)  # Удаляем старые таблицы
Base.metadata.create_all(engine) # Создаем новые

product = Products(name="Apple", price=100, category_id=1, description="Свежее яблоко")
category = Category(name="Fruits")

session.add(category)  # Добавляем категорию
session.add(product)   # Добавляем продукт
session.commit()       # Сохраняем изменения

# Запрос всех продуктов
products = session.query(Products).all()

# Запрос категории с id=1
category = session.query(Category).filter_by(id=1).first()

product = session.query(Products).filter_by(name="Apple").first()
if product:  # Проверяем, что продукт существует
    product.price = 120  # Обновляем цену
    session.commit()     # Сохраняем изменения

category = session.query(Category).get(1)
if category:
    session.delete(category)
    session.commit()

#Создайте новый продукт
product = Products(name='Апельсин', price=76, description="Сочные", category_id=1)
session.add(product)
session.commit()

f = 4