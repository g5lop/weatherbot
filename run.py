import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

print(aiohttp.__version__)
BOT_TOKEN = "8316678625:AAGlffkcKYD44SjTkWuFd6xUO3q6Naoe40E"  # вставь сюда токен от @BotFather

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

async def get_weather(city: str = "Ulyanovsk") -> str:
    """
    Получает погоду из wttr.in в текстовом виде.
    """
    url = f"https://wttr.in/{city}?format=3"  
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.text()
            else:
                return "⚠️ Не удалось получить погоду."

@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Ульяновск", callback_data="city_Ульяновск"),
                InlineKeyboardButton(text="Инза", callback_data="city_Инза"),
                InlineKeyboardButton(text="Димитровград", callback_data="city_Димитровград")
            ]
        ]
    )
    await message.answer(
        "Привет! ☀️\n"
        "Выбери город, чтобы узнать погоду.",
        reply_markup=keyboard
    )

@dp.callback_query(lambda query: query.data.startswith("city_"))
async def city_callback(callback_query: types.CallbackQuery):
    city = callback_query.data.split("_")[1]
    weather_info = await get_weather(city)
    await callback_query.message.answer(f"Погода в {city}:\n{weather_info}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())