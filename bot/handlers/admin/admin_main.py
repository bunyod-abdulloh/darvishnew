from aiogram import Router, types, F
from aiogram.filters import Command

from bot.filters import IsBotAdminFilter
from bot.keyboards.reply.admin_dkb import admin_main_dkb
from data.config import ADMINS

router = Router()


@router.message(IsBotAdminFilter(ADMINS), Command("admin"))
async def admin_main_router(message: types.Message):
    await message.answer(
        text=message.text, reply_markup=admin_main_dkb
    )


@router.message(IsBotAdminFilter(ADMINS), F.text == "Admin bosh sahifasi")
async def admin_back_main_router(message: types.Message):
    await message.answer(
        text=message.text, reply_markup=admin_main_dkb
    )
