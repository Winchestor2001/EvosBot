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
        KeyboardButton(text="⚙️ Настройки")
        )

    return btn
