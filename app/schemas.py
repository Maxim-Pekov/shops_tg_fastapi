from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CreateProduct(BaseModel):
    name: str
    description: str
    image_url: str
    category: int | str
    store_name: str
    is_active: bool
    price: float
    created_at: Optional[datetime] = None


class CreateCategory(BaseModel):
    name: str
    parent_id: int | None
    slug: str


class CreateUser(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str
    telegram: str


class CreateStore(BaseModel):
    name: str
    address: str
    is_active: bool
    slug: Optional[str] = None