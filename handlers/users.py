from loader import dp
from aiogram.types import Message, CallbackQuery
from db.database import add_user, set_lang, get_user_lang
from keyboards.reply_btn import start_command_btn, choose_lang_btn, settings_btn, location_btn, yes_or_no_location_btn
from states import UserStates
from aiogram.dispatcher.storage import FSMContext
from bot_context import languages


@dp.message_handler(commands=['start'])
async def start_command(message: Message):
    have_lang = await add_user(
        user_id=message.from_user.id,
        username=message.from_user.username
    )
    if have_lang:
        btn = await choose_lang_btn()
        await message.answer(f"Tilni tanlang\n\nВыберите язык:", reply_markup=btn)
        await UserStates.choose_lang.set()
    else:
        lang = await get_user_lang(user_id=message.from_user.id)
        btn = await start_command_btn(lang)
        await message.answer(languages[lang]['start_command_text'], reply_markup=btn)


@dp.message_handler(state=UserStates.choose_lang)
async def choose_lang_state(message: Message, state: FSMContext):
    text = message.text

    if text == '🇺🇿 UZ':
        lang = "uz"        
    else:
        lang = "ru"

    await set_lang(
        user_id=message.from_user.id,
        lang=lang
    )
    await start_command(message)
    await state.finish()



@dp.message_handler(text=['⚙️ Sozlamalar', '⚙️ Настройки'])
async def user_settings_handler(message: Message):
    lang = await get_user_lang(user_id=message.from_user.id)
    btn = await settings_btn(lang=lang)
    await message.answer(languages[lang]['change_lang_text'], reply_markup=btn)


@dp.message_handler(text=['Tilni o`zgartirish', 'Изменить язык'])
async def change_lang_handler(message: Message, state: FSMContext):
    btn = await choose_lang_btn()
    await message.answer(f"Tilni tanlang\n\nВыберите язык:", reply_markup=btn)
    await UserStates.choose_lang.set()


@dp.message_handler(text=["🍴 Menu", '🍴 Меню'])
async def menu_commad_handler(message: Message):
    lang = await get_user_lang(user_id=message.from_user.id)
    btn = await location_btn(lang)
    await message.answer(languages[lang]['location_text'], reply_markup=btn)


# text, photo, video, sticker, location, voice, audio, contact, animation
@dp.message_handler(content_types=['location', 'text'])
async def get_user_location_handler(message: Message):
    if message.text in ['⬅️ Ortga', '⬅️ Назад', '❌ Yo`q', '❌ Yo`q']:
        await menu_commad_handler(message)
        return
    lang = await get_user_lang(user_id=message.from_user.id)
    btn = await yes_or_no_location_btn(lang)
    await message.answer(languages[lang]['is_correct_location'], reply_markup=btn)
