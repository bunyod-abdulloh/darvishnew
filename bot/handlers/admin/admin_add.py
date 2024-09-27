import asyncio

import asyncpg
from aiogram import Router, types, F

from data.jsonfiles.articlesjson import articlesjson
from data.jsonfiles.suhbatloyihajson import suhbatloyiha
from data.jsonfiles.usersjson import users
from loader import db

router = Router()


@router.message(F.text == "addusers")
async def add_user_handler(message: types.Message):
    c = 0
    await message.answer(
        text="Foydalanuvchilarni qo'shish boshlandi!"
    )
    try:
        for user in users:
            c += 1
            await db.add_user_json(
                full_name=user['full_name'],
                username=user['username'],
                telegram_id=user['telegram_id'],
                fio=user['fio'],
                phone=user['phone']
            )
            await asyncio.sleep(0.05)
        await message.answer(
            text=f"{c} ta foydalanuvchi qo'shildi"
        )
    except asyncpg.exceptions.UniqueViolationError:
        pass
    except Exception as e:
        await message.answer(
            text=f"Xatolik: {e}"
        )


@router.message(F.text == "addprojects")
async def add_projects_handler(message: types.Message):
    c = 0
    for project in suhbatloyiha:
        c += 1
        await db.add_projects(
            category=project['category'],
            subcategory=project['subcategory'],
            sequence=project['sequence'],
            file_type=project['file_type'],
            file_id=project['file_id'],
            caption=project['caption']
        )
    await message.answer(
        text=f"{c} ta material qo'shildi"
    )


@router.message(F.text == "addarticles")
async def add_articles_handler(message: types.Message):
    c = 0
    for article in articlesjson:
        c += 1
        await db.add_articles(
            file_name=article['file_name'],
            link=article['link']
        )
    await message.answer(
        text=f"{c} ta maqola qo'shildi"
    )
