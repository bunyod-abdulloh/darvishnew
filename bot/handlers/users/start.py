from aiogram import Router, types, F
from aiogram.filters import CommandStart

from bot.keyboards.reply.main_dkb import main_dkb
from loader import db

router = Router()


@router.message(CommandStart())
async def do_start(message: types.Message):
    telegram_id = message.from_user.id
    full_name = message.from_user.full_name
    username = message.from_user.username
    try:
        await db.add_user(telegram_id=telegram_id, full_name=full_name, username=username)
    except Exception:
        pass
    await message.answer(f"Assalomu alaykum {full_name}!\n\nBotimizga xush kelibsiz!!!", reply_markup=main_dkb)


@router.message(F.text == "🏡 Bosh sahifa")
async def back_main_menu(message: types.Message):
    await message.answer(
        text=message.text, reply_markup=main_dkb
    )
