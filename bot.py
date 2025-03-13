import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv

# Загружаем токен бота из .env
load_dotenv()
TOKEN = os.getenv("7843959820:AAFvfy9Sk5U5TZqP3aeRGBxH-qd2t1eloQE")

# Настройка бота
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Начальные параметры
GOAL_AMOUNT = 70000  # Цель по деньгам
DAYS_LIMIT = 16  # Сколько дней на выполнение
progress = {"earned": 0}

# Список советов по продуктивности
TIPS = [
    "Не отвлекайся на соцсети — лучше заработай ещё немного!",
    "Разбей задачу на маленькие шаги и сделай первый прямо сейчас.",
    "Отдых тоже важен! Но только после хорошей работы.",
    "Используй технику Помодоро: 25 минут работы, 5 минут отдыха.",
    "Не бойся просить больше денег за свой труд!",
    "Занимайся самодисциплиной — это ключ к успеху.",
    "Фокусируйся на важных задачах, а не на срочных."
]

# Команда для добавления заработанных денег
@dp.message(Command("money"))
async def add_money(message: Message):
    try:
        amount = int(message.text.split()[1])
        progress["earned"] += amount
        await message.reply(f"💰 Денчик заработал {amount} р.! Всего: {progress['earned']} р.")
    except (IndexError, ValueError):
        await message.reply("Ошибка! Используй формат: /money X, где X - сумма.")

# Команда для проверки прогресса
@dp.message(Command("status"))
async def check_status(message: Message):
    remaining_money = GOAL_AMOUNT - progress["earned"]
    remaining_days = DAYS_LIMIT - (message.date.day % DAYS_LIMIT)  # Пример расчета дней
    
    if remaining_money <= 0:
        await message.reply("🔥 Денчик достиг цели! Молодец!")
    else:
        await message.reply(f"📊 Осталось заработать: {remaining_money} р.\n⏳ Дней до конца: {remaining_days}")

# Команда для мотивационного совета
@dp.message(Command("god"))
async def get_tip(message: Message):
    from random import choice
    tip = choice(TIPS)
    await message.reply(f"🧠 Совет дня: {tip}")

# Запуск бота
async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
