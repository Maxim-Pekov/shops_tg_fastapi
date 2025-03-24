import time

import uvicorn

from fastapi import FastAPI

from app.backend.db import Base, engine
# from app.models import store
from app.models import Product
from celery_app import celery
from routers import category, products, auth, store
from app.daemons.five.products_parser import product_parser, categories_parser

fastapi_app = FastAPI()


@celery.task                               # просто оборачиваем функцию в декоратор
def call_background_task():
    time.sleep(10)
    print(f"Background Task called!")


@fastapi_app.get("/")
async def welcome() -> dict:
    # call_background_task.delay()
    product_parser("fff")
    # categories_parser()
    # Product.get_all_product_by_name("mолоко")
    return {"message": "My e-commerce app"}


fastapi_app.include_router(category.router)
fastapi_app.include_router(products.router)
fastapi_app.include_router(auth.router)
fastapi_app.include_router(store.router)


if __name__ == "__main__":

    Base.metadata.create_all(engine)

    uvicorn.run("main:fastapi_app", port=8000, host="0.0.0.0", reload=True)
