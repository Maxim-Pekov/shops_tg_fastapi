from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from slugify import slugify
# from sqlalchemy import select, insert, update
# from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from sqlalchemy.orm import Session
from backend.db_depends import get_db
from app.models import Category
from schemas import CreateCategory

from app.backend.db import Base, engine

router = APIRouter(prefix='/category', tags=['category'])


@router.get('/all_categories')
def get_all_categories(db: Session = Depends(get_db)):
    return Category.get_all_categories(db)


@router.post('/create')
def create_category(create_category: CreateCategory, db: Session = Depends(get_db)):
    Category.create_categories(db, create_category)
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }

#
# @router.put('/update_category')
# async def update_category(db: Annotated[AsyncSession, Depends(get_db)], category_id: int, update_category: CreateCategory):
#     category = await db.scalar(select(Category).where(Category.id == category_id))
#     if category is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail='There is no category found'
#         )
#
#     await db.execute(update(Category).where(Category.id == category_id).values(
#             name=update_category.name,
#             slug=slugify(update_category.name),
#             parent_id=update_category.parent_id))
#
#
#     await db.commit()
#     return {
#         'status_code': status.HTTP_200_OK,
#         'transaction': 'Category update is successful'
#     }
#
#
# @router.delete('/delete')
# async def delete_category(db: Annotated[AsyncSession, Depends(get_db)], category_id: int):
#     category = await db.scalar(select(Category).where(Category.id == category_id))
#     if category is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail='There is no category found'
#         )
#     await db.execute(update(Category).where(Category.id == category_id).values(is_active=False))
#     await db.commit()
#     return {
#         'status_code': status.HTTP_200_OK,
#         'transaction': 'Category delete is successful'
#     }