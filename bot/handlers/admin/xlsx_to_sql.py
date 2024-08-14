import os

import pandas as pd
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from data.config import ADMINS
from bot.filters import IsBotAdminFilter
from loader import db, bot
from bot.states import AdminState

router = Router()


async def download_and_save_file(file_id: str, save_path: str):
    file_info = await bot.get_file(file_id)
    f_path = os.path.join(save_path, file_info.file_path)
    os.makedirs(os.path.dirname(f_path), exist_ok=True)

    await bot.download_file(file_info.file_path, f_path)

    return f_path


@router.message(F.text == "admintest", IsBotAdminFilter(ADMINS))
async def add_test(message: types.Message, state: FSMContext):
    await message.answer(
        text="Test qo'shish uchun Excel faylni yuboring"
    )
    await state.set_state(AdminState.add_test)


@router.message(F.document, AdminState.add_test)
async def add_test_questions(message: types.Message, state: FSMContext):
    # await message.answer(
    #     text="Test qo'shish o'chirilgan!"
    # )
    f_path = await download_and_save_file(
        file_id=message.document.file_id, save_path="downloads/"
    )
    df = pd.read_excel(f_path, sheet_name=0)
    c = 0
    for row in df.values:
        # await db.add_questions_yaxin(
        #     scale_type=row[0],
        #     question=row[1],
        #     a=row[2],
        #     b=row[3],
        #     c=row[4],
        #     d=row[5],
        #     e=row[6]
        # )
        # await db.add_yaxin_scales(
        #     scale_type=row[0],
        #     question_number=row[1],
        #     point_one=row[2],
        #     point_two=row[3],
        #     point_three=row[4],
        #     point_four=row[5],
        #     point_five=row[6]
        # )
        # await db.add_leoquestions(
        #     question_number=row[0],
        #     question=row[1]
        # )
        # await db.add_leoscales(
        #     scale_type=row[0],
        #     yes=row[1],
        #     no_=row[2]
        # )
        # await db.add_ayztempquestion(
        #     question_number=row[0],
        #     question=row[1]
        # )
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
