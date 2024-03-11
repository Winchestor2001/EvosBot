from loader import dp
from aiogram import executor


async def on_startup(dispatcher):
    import handlers.users



if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)