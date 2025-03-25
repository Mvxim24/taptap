import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

TOKEN = "7548796569:AAE432a3Y5_gYWcitBWl-B3Ho95U7b2VWN8"  # Замени на свой токен

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Словарь для хранения рекордов пользователей
user_scores = {}

@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Играть 🎮", web_app=WebAppInfo(url="https://yourdomain.com/game.html"))]
        ]
    )
    await message.answer("Привет! Играй в тапалку и ставь рекорды!", reply_markup=keyboard)

@dp.message(Command("score"))
async def show_score(message: types.Message):
    user_id = message.from_user.id
    best_score = user_scores.get(user_id, 0)
    await message.answer(f"Твой рекорд: {best_score} тапов!")

@dp.message()
async def receive_score(message: types.Message):
    user_id = message.from_user.id
    try:
        data = int(message.text)  # Ожидаем число (результат игры)
        best_score = user_scores.get(user_id, 0)
        if data > best_score:
            user_scores[user_id] = data
            await message.answer(f"Новый рекорд: {data} тапов! 🎉")
        else:
            await message.answer(f"Ты набрал {data} тапов. Твой рекорд: {best_score}.")

    except ValueError:
        await message.answer("Отправь число — количество тапов!")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    dp.run_polling(bot)
