from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from slugify import slugify
# from sqlalchemy import select, insert, update
# from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from app.models import Category
from app.models.store import Store
from app.schemas import CreateCategory, CreateStore

from app.backend.db import Base, engine

router = APIRouter(prefix='/store', tags=['store'])


@router.get('/all_stories')
def get_all_stores(db: Session = Depends(get_db)):
    return Store.get_all_stories(db)


@router.post('/create')
def create_store(create_store: CreateStore, db: Session = Depends(get_db)):
    Store.create_store(db, create_store)
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }