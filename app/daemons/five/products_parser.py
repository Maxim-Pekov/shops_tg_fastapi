import asyncio

import requests

# from backend import db
from app.celery_app import celery
from slugify import slugify
from sqlalchemy import insert, select, update
from backend.db_depends import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Category, Product
from app.schemas import CreateProduct, CreateCategory
from app.backend.db import SessionLocal


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
    parent_category_name = products_json.get('name')
    subcategories = products_json.get('subcategories', {})
    db = SessionLocal()
    for subcategory in subcategories:
        category = CreateCategory(
            name=subcategory.get("name"),
            parent_id=Category.get_category_by_name(db, parent_category_name).id,
        )
        category = Category.get_or_create_category_by_name(db, category)
        products = subcategory.get("products", [])
        for _product in products:
            product = CreateProduct(
                name=_product['name'],
                price=_product['prices']['regular'],
                category=category.id,
                is_active=True,
                store_name='five',
                image_url='',
                description=''
            )
            Product.create_or_update_product(db, product)


@celery.task
def categories_parser():
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'origin': 'https://5ka.ru',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        'x-app-version': '0.1.1.dev',
        'x-device-id': 'd9d0b147-be63-4a51-acc2-800b1c9f0371',
        'x-platform': 'webapp',
    }

    params = {
        'mode': 'delivery',
        'include_subcategories': '1',
    }

    response = requests.get(
        'https://5d.5ka.ru/api/catalog/v1/stores/36JP/categories',
        params=params,
        headers=headers,
    )
    db = SessionLocal()
    categories_json = response.json()
    for category in categories_json:
        category = CreateCategory(
            name=category.get("name"),
            parent_id=None,
        )
        Category.create_categories(db, category)


celery.conf.beat_schedule = {
    'run-me-background-task': {
        'task': 'daemons.five.products_parser.product_parser',
        'schedule': 30.0,                              # запуск задачи каждые 60 секунд
        'args': ('Test text message',)
    }
}