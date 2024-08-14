import os

from aiogram import Router, F, types
from data.config import ADMINS
from bot.filters import IsBotAdminFilter
from bot.keyboards.reply.admin_dkb import admin_download_dkb
from loader import db
from utils.pgtoexcel import export_to_excel

router = Router()


@router.message(IsBotAdminFilter(ADMINS), F.text == "Excel yuklab olish")
async def download_router(message: types.Message):
    await message.answer(
        text=message.text, reply_markup=admin_download_dkb
    )


@router.message(IsBotAdminFilter(ADMINS), F.text == "Kurslar")
async def upload_courses_router(message: types.Message):
    await message.answer(
        text="Bo'lim hozircha ishlamaydi!"
    )
    # all_courses = await db.select_all_tables(
    #     table_type='kurs'
    # )
    #
    # file_path = f"data/kurslar.xlsx"
    # wb = Workbook()
    # ws = wb.active
    # ws.append(['Kurs nomi', 'Dars tartib raqami', 'Audio ID', 'Rasm ID', 'Video ID', 'Document ID', 'Fayl nomi',
    #            'Tavsif'])


@router.message(IsBotAdminFilter(ADMINS), F.text == "Dars va kurslar jadvali")
async def upload_lessons_and_courses_router(message: types.Message):
    all_tables = await db.select_table_tables()

    file_path = f"data/jadvallar_royxati.xlsx"

    await export_to_excel(
        data=all_tables, headings=['Tartib raqami', 'Nomi', 'Turi', 'Kanal ID raqami', 'Izohlar', 'Check'],
        filepath=file_path
    )
    await message.answer_document(types.input_file.FSInputFile(file_path))
    os.remove(file_path)


@router.message(IsBotAdminFilter(ADMINS), F.text == "Maqolalar")
async def upload_articles_router(message: types.Message):
    all_articles = await db.select_all_articles()

    file_path = f"data/maqolalar.xlsx"
    await export_to_excel(
        data=all_articles, headings=['ID', 'Maqola nomi', 'Maqola linki'], filepath=file_path
    )
    await message.answer_document(
        document=types.input_file.FSInputFile(file_path)
    )
    os.remove(file_path)


@router.message(IsBotAdminFilter(ADMINS), F.text == "Suhbat va loyihalar")
async def upload_interviews_router(message: types.Message):
    all_interviews = await db.select_all_projects()

    file_path = f"data/suhbat_loyiha.xlsx"
    await export_to_excel(
        data=all_interviews, headings=['ID', 'Tartib raqami', 'Audio ID', 'Photo ID', 'Video ID', 'Document ID',
                                       'Kategoriya', 'Subkategoriya', 'Tavsif', 'Youtube link'], filepath=file_path
    )
    await message.answer_document(types.input_file.FSInputFile(file_path))
    os.remove(file_path)


@router.message(IsBotAdminFilter(ADMINS), F.text == "Foydalanuvchilar yuklash")
async def upload_users_router(message: types.Message):
    users = await db.select_all_users()

    file_path = f"data/foydalanuvchilar.xlsx"
    await export_to_excel(data=users, headings=['ID', 'Full Name', 'Username', 'Telegram ID'], filepath=file_path)

    await message.answer_document(types.input_file.FSInputFile(file_path))
    os.remove(file_path)
