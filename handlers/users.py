from loader import dp
from aiogram.types import Message, CallbackQuery
from db.database import add_user
from keyboards.reply_btn import start_command_btn


@dp.message_handler(commands=['start'])
async def start_command(message: Message):
    have_lang = await add_user(
        user_id=message.from_user.id,
        username=message.from_user.username
    )
    if have_lang:
        await message.answer(f"Tilni tanlang\n\nВыберите язык:")
    else:
        btn = await start_command_btn('uz')
        await message.answer(f'Salom', reply_markup=btn)


