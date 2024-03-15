from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot_context import languages


async def start_command_btn(lang: str):
    btn = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn.row(
        KeyboardButton(text=languages[lang]['buttons']['menu_text'])
        )
    btn.row(
        KeyboardButton(text=languages[lang]['buttons']['my_orders_text'])
        )
    btn.row(
        KeyboardButton(text="✍️ Оставить отзыв"), 
        KeyboardButton(text=languages[lang]['buttons']['settings_text'])
        )

    return btn


async def choose_lang_btn():
    btn = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn.add(
        KeyboardButton(text="🇺🇿 UZ"),
        KeyboardButton(text="🇷🇺 RU"),
    )
    return btn


async def settings_btn(lang: str):
    btn = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn.add(
        KeyboardButton(text=languages[lang]['buttons']['change_lang_text']),
        KeyboardButton(text=languages[lang]['buttons']['back_text']),
    )
    return btn



