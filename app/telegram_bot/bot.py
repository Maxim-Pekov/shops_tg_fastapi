import asyncio
import logging
import os

from dotenv import load_dotenv
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher


load_dotenv()
tg_token = os.getenv('TG_API_BOT')
bot = Bot(token=tg_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nНапиши мне названия продуктов которые ты хочешь купить!")


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Напиши мне что-нибудь, и я отпрпавлю этот текст тебе в ответ!")


@dp.message_handler()
async def echo_message(msg: types.Message):
    response = requests.get(
        f'http://127.0.0.1:8000/products/search_by_name/{msg.text}',
    )
    response.raise_for_status()
    products = [f"{product.get('name')}\n" for product in response.json()]
    if products:
        first_product = response.json()[0].get('name')

        # Создаем инлайн-кнопку
        keyboard = InlineKeyboardMarkup()
        button = InlineKeyboardButton(text=first_product, callback_data=f"product_1")
        keyboard.add(button)

        # Отправляем сообщение с кнопкой
        await bot.send_message(
            msg.from_user.id,
            "Вот первый продукт из найденных:",
            reply_markup=keyboard
        )
    else:
        await bot.send_message(msg.from_user.id, "Продукты не найдены.")

if __name__ == '__main__':
    executor.start_polling(dp)