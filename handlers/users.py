from loader import dp
from aiogram.types import Message, CallbackQuery


@dp.message_handler(commands=['start'])
async def start_command(message: Message):
    await message.answer(f'Salom')


