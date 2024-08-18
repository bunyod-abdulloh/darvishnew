import os

import pandas as pd
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from bot.filters import IsBotAdminFilter
from bot.states import AdminState
from data.config import ADMINS
from loader import db, bot

router = Router()


async def download_and_save_file(file_id: str, save_path: str):
    file_info = await bot.get_file(file_id)
    f_path = os.path.join(save_path, file_info.file_path)
    os.makedirs(os.path.dirname(f_path), exist_ok=True)

    await bot.download_file(file_info.file_path, f_path)

    return f_path


@router.message(F.text == "yaxinquestions", IsBotAdminFilter(ADMINS))
async def add_yaxquest_handler(message: types.Message, state: FSMContext):
    await message.answer(
        text="Test qo'shish uchun Excel faylni yuboring"
    )
    await state.set_state(AdminState.yaxinquestions)


@router.message(F.document, AdminState.yaxinquestions)
async def add_yaxquest_state(message: types.Message, state: FSMContext):
    f_path = await download_and_save_file(
        file_id=message.document.file_id, save_path="downloads/"
    )
    df = pd.read_excel(f_path, sheet_name=0)
    c = 0
    for row in df.values:
        await db.add_questions_yaxin(
            scale_type=row[0],
            question=row[1],
            a=row[2],
            b=row[3],
            c=row[4],
            d=row[5],
            e=row[6]
        )
        c += 1
    await message.answer(
        text=f"Jami {c} ta savollar qo'shildi"
    )
    await state.clear()
    os.remove(f_path)


@router.message(F.text == "yaxinscales", IsBotAdminFilter(ADMINS))
async def add_yaxscales_handler(message: types.Message, state: FSMContext):
    await message.answer(
        text="Test qo'shish uchun Excel faylni yuboring"
    )
    await state.set_state(AdminState.yaxinscales)


@router.message(F.document, AdminState.yaxinscales)
async def add_yaxscales_state(message: types.Message, state: FSMContext):
    f_path = await download_and_save_file(
        file_id=message.document.file_id, save_path="downloads/"
    )
    df = pd.read_excel(f_path, sheet_name=0)
    c = 0
    for row in df.values:
        await db.add_yaxin_scales(
            scale_type=row[0],
            question_number=row[1],
            point_one=row[2],
            point_two=row[3],
            point_three=row[4],
            point_four=row[5],
            point_five=row[6]
        )
        c += 1
    await message.answer(
        text=f"Jami {c} ta savollar qo'shildi"
    )
    await state.clear()
    os.remove(f_path)


@router.message(F.text == "leoquestions", IsBotAdminFilter(ADMINS))
async def add_leoquest_handler(message: types.Message, state: FSMContext):
    await message.answer(
        text="Test qo'shish uchun Excel faylni yuboring"
    )
    await state.set_state(AdminState.leoquestions)


@router.message(F.document, AdminState.leoquestions)
async def add_leoquest_state(message: types.Message, state: FSMContext):
    f_path = await download_and_save_file(
        file_id=message.document.file_id, save_path="downloads/"
    )
    df = pd.read_excel(f_path, sheet_name=0)
    c = 0
    for row in df.values:
        await db.add_leoquestions(
            question_number=row[0],
            question=row[1]
        )
        c += 1
    await message.answer(
        text=f"Jami {c} ta savollar qo'shildi"
    )
    await state.clear()
    os.remove(f_path)


@router.message(F.text == "leoscales", IsBotAdminFilter(ADMINS))
async def add_leoscales_handler(message: types.Message, state: FSMContext):
    await message.answer(
        text="Test qo'shish uchun Excel faylni yuboring"
    )
    await state.set_state(AdminState.leoscales)


@router.message(F.document, AdminState.leoscales)
async def add_leoscales_state(message: types.Message, state: FSMContext):
    f_path = await download_and_save_file(
        file_id=message.document.file_id, save_path="downloads/"
    )
    df = pd.read_excel(f_path, sheet_name=0)
    c = 0
    for row in df.values:
        await db.add_leoscales(
            scale_type=row[0],
            yes=row[1],
            no_=row[2]
        )
        c += 1
    await message.answer(
        text=f"Jami {c} ta savollar qo'shildi"
    )
    await state.clear()
    os.remove(f_path)


@router.message(F.text == "ayzquestion")
async def add_ayzquestion_handler(message: types.Message, state: FSMContext):
    await message.answer(
        text="Test qo'shish uchun Excel faylni yuboring"
    )
    await state.set_state(AdminState.ayzquestions)


@router.message(AdminState.ayzquestions)
async def add_ayzquestion_state(message: types.Message, state: FSMContext):
    f_path = await download_and_save_file(
        file_id=message.document.file_id, save_path="downloads/"
    )
    df = pd.read_excel(f_path, sheet_name=0)
    c = 0
    for row in df.values:
        await db.add_ayztempquestion(
            question_number=row[0],
            question=row[1]
        )
        c += 1
    await message.answer(
        text=f"Jami {c} ta savollar qo'shildi"
    )
    await state.clear()
    os.remove(f_path)


@router.message(F.text == "ayzscales")
async def add_ayzscales_handler(message: types.Message, state: FSMContext):
    await message.answer(
        text="Test qo'shish uchun Excel faylni yuboring"
    )
    await state.set_state(AdminState.ayzscales)


@router.message(AdminState.ayzscales)
async def add_ayzscales_state(message: types.Message, state: FSMContext):
    f_path = await download_and_save_file(
        file_id=message.document.file_id, save_path="downloads/"
    )
    df = pd.read_excel(f_path, sheet_name=0)
    c = 0
    for row in df.values:
        await db.add_ayztempscales(
            scale_type=row[0],
            yes=row[1],
            no_=row[2]
        )
        c += 1
    await message.answer(
        text=f"Jami {c} ta savollar qo'shildi"
    )
    await state.clear()
    os.remove(f_path)
