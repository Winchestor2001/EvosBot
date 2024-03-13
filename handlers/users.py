from loader import dp
from aiogram.types import Message, CallbackQuery
from db.database import add_user, set_lang, get_user_lang
from keyboards.reply_btn import start_command_btn, choose_lang_btn


@dp.message_handler(commands=['start'])
async def start_command(message: Message):
    have_lang = await add_user(
        user_id=message.from_user.id,
        username=message.from_user.username
    )
    if have_lang:
        btn = await choose_lang_btn()
        await message.answer(f"Tilni tanlang\n\nВыберите язык:", reply_markup=btn)
    else:
        btn = await start_command_btn('uz')
        await message.answer(f'Salom', reply_markup=btn)


@dp.message_handler(text=['🇺🇿 UZ', '🇷🇺 RU'])
async def choose_lang_handler(message: Message):
    text = message.text

    if text == '🇺🇿 UZ':
        lang = "uz"        
    else:
        lang = "ru"

    await set_lang(
        user_id=message.from_user.id,
        lang=lang
    )

