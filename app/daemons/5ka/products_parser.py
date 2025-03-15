import asyncio

import requests

# from backend import db
from app.celery_app import celery
from slugify import slugify
from sqlalchemy import insert, select, update

from app.models import Category, Product
from app.schemas import CreateProduct
# from celery import shared_task

@celery.task
def product_parser(text):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'origin': 'https://5ka.ru',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'x-app-version': '0.1.1.dev',
        'x-device-id': 'd9d0b147-be63-4a51-acc2-800b1c9f0371',
        'x-platform': 'webapp',
    }

    params = {
        'mode': 'delivery',
        'include_restrict': 'false',
        'preview_products_count': '6',
    }

    response = requests.get(
        'https://5d.5ka.ru/api/catalog/v1/stores/36JP/categories/73C2336/preview',
        params=params,
        headers=headers,
    )
    products_json = response.json()

    subcategories = products_json.get('subcategories', {})
    from app.backend.db import sessionmaker
    milks = []
    for subcategory in subcategories:
        print(subcategory.get("name", ""))
        if subcategory.get("name", "") == 'Молоко':
            milks = subcategory.get("products", [])
    with async_session_maker() as session:
        for milk in milks:
            product = CreateProduct(
                name=milk['name'],
                price=milk['prices']['regular'],
                category=19,
                is_active=True,
                stock=10,
                image_url='',
                description=''
            )
            print(product)
            product_slug = slugify(product.name)
            product_update = await session.scalar(select(Product).where(Product.slug == product_slug))
            if product_update is None:
                stmt = insert(Product).values(
                    name=product.name,
                    description=product.description,
                    price=product.price,
                    image_url=product.image_url,
                    stock=product.stock,
                    category_id=product.category,
                    rating=0.0,
                    slug=product_slug
                )
            else:
                stmt = update(Product).where(Product.slug == product_slug).values(
                    name=product.name,
                    description=product.description,
                    price=product.price,
                    image_url=product.image_url,
                    stock=product.stock,
                    category_id=product.category,
                    slug=slugify(product.name)
                )
            await session.execute(stmt)
        await session.commit()


celery.conf.beat_schedule = {
    'run-me-background-task': {
        'task': 'daemons.5ka.products_parser.product_parser',
        'schedule': 30.0,                              # запуск задачи каждые 60 секунд
        'args': ('Test text message',)
    }
}