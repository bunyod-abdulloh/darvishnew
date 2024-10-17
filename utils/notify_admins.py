import logging

from aiogram import Bot


async def on_startup_notify(bot: Bot):
    try:
        await bot.send_message(
            chat_id=-1001399496245,
            text="Bot ishga tushdi")
    except Exception as err:
        logging.exception(err)
