from loader import dp
from aiogram.types import Message, CallbackQuery
from db.database import add_user, set_lang, get_user_lang, get_all_categories, get_products, get_product_info
from keyboards.reply_btn import start_command_btn, choose_lang_btn, settings_btn, location_btn, yes_or_no_location_btn, categories_btn, products_btn, product_btn, back_btn
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


@dp.message_handler(content_types=['text'], state=UserStates.choose_category)
async def choose_category_state(message: Message, state: FSMContext):
    lang = await get_user_lang(user_id=message.from_user.id)

    if message.text in ['⬅️ Ortga', '⬅️ Назад']:
        categories = await get_all_categories()
        btn = await categories_btn(categories, lang)
        await message.answer(languages[lang]['choose_category_text'], reply_markup=btn)
        await UserStates.choose_category.set()
    else:
        category_products, category_img = await get_products(category=message.text)
        btn = await products_btn(category_products, lang)
        await message.answer_photo(category_img, reply_markup=btn)
        await UserStates.choose_product.set()


@dp.message_handler(content_types=['text'], state=UserStates.choose_product)
async def choose_product_state(message: Message, state: FSMContext):
    lang = await get_user_lang(user_id=message.from_user.id)
    product_info = await get_product_info(product=message.text)
    context = f"{product_info[1]}\n{product_info[2]}\n\n{product_info[3]}"

    btn = await back_btn(lang)
    await message.answer("⏳", reply_markup=btn)
    btn = await product_btn()
    await message.answer_photo(product_info[4], caption=context, reply_markup=btn)
    await state.finish()


# text, photo, video, sticker, location, voice, audio, contact, animation
@dp.message_handler(content_types=['location', 'text'])
async def get_user_location_handler(message: Message):
    lang = await get_user_lang(user_id=message.from_user.id)

    if message.text in ['⬅️ Ortga', '⬅️ Назад', '❌ Yo`q', '❌ Нет']:
        await menu_commad_handler(message)
        return

    elif message.text in ['✅ Xa', '✅ Да']:
        categories = await get_all_categories()
        btn = await categories_btn(categories, lang)
        await message.answer(languages[lang]['choose_category_text'], reply_markup=btn)
        await UserStates.choose_category.set()
        return
    
    elif message.content_type == 'location':
        btn = await yes_or_no_location_btn(lang)
        await message.answer(languages[lang]['is_correct_location'], reply_markup=btn)
