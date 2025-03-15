from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import select, insert
from app.models.users import User
from app.schemas import CreateUser
from backend.db_depends import get_db
from typing import Annotated
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix='/auth', tags=['auth'])
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


@router.post('/')
async def create_user(db: Annotated[AsyncSession, Depends(get_db)], create_user: CreateUser):
    await db.execute(insert(User).values(first_name=create_user.first_name,
                                         last_name=create_user.last_name,
                                         username=create_user.username,
                                         email=create_user.email,
                                         telegram=create_user.telegram,
                                         hashed_password=bcrypt_context.hash(create_user.password),
                                         ))
    await db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


async def authanticate_user(db: Annotated[AsyncSession, Depends(get_db)], username: str, password: str):
    user = await db.scalar(select(User).where(User.username == username))
    if not user or not bcrypt_context.verify(password, user.hashed_password) or user.is_active == False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
