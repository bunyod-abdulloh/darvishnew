import aiogram.exceptions
from aiogram import Router, F, types

from bot.handlers.functions.functions_one import extracter
from bot.keyboards.inline.buttons import key_returner_projects
from bot.keyboards.reply.interviews_reply import interviews_cbuttons
from data.jsonfiles.suhbatloyihajson import suhbatloyiha
from loader import db

interviews_projects = Router()


async def prev_next_projects_func(extract, call: types.CallbackQuery, current_page, all_pages):
    items = extract[current_page - 1]
    projects = str()

    for n in items:
        projects += f"{n['rank']}. {n['category']}\n"
    markup = key_returner_projects(
        items=items, current_page=current_page, all_pages=all_pages
    )
    try:
        await call.message.edit_text(
            text=projects, reply_markup=markup
        )
    except aiogram.exceptions.TelegramBadRequest:
        pass


@interviews_projects.message(F.text == "addpr")
async def add_project_handler(message: types.Message):
    c = 0
    for n in suhbatloyiha:
        c += 1
        sequence = n['sequence']
        file_id = n['file_id']
        file_type = n['file_type']
        category = n['category']
        subcategory = n['subcategory']
        caption = n['caption']
        await db.add_projects(
            sequence=sequence,
            file_id=file_id,
            file_type=file_type,
            category=category,
            subcategory=subcategory,
            caption=caption
        )
    await message.answer(
        text=f"{c} ta material qo'shildi""'"
    )


@interviews_projects.message(F.text == "🎙 Suhbat va loyihalar")
async def interviews_projects_hr_one(message: types.Message):
    all_projects = await db.select_projects()
    if all_projects:
        extract = extracter(all_medias=all_projects, delimiter=10)
        current_page = 1
        all_pages = len(extract)
        items = extract[current_page - 1]
        projects = str()

        for n in items:
            projects += f"{n['rank']}. {n['category']}\n"
        markup = key_returner_projects(
            items=items, current_page=current_page, all_pages=all_pages
        )
        await message.answer(
            text=message.text, reply_markup=interviews_cbuttons
        )
        await message.answer(
            text=projects, reply_markup=markup
        )
    else:
        await message.answer(
            text="Hozircha suhbat va loyihalar bo'limi ishga tushmadi!"
        )


@interviews_projects.callback_query(F.data.startswith("prev_projects:"))
async def interviews_projects_hr_prev(call: types.CallbackQuery):
    await call.answer(
        cache_time=0
    )
    all_projects = await db.select_projects()
    extract = extracter(
        all_medias=all_projects, delimiter=10
    )
    current_page = int(call.data.split(':')[1])
    all_pages = len(extract)

    if current_page == 1:
        current_page = all_pages
    else:
        current_page -= 1
    await prev_next_projects_func(
        extract=extract, call=call, current_page=current_page, all_pages=all_pages
    )


@interviews_projects.callback_query(F.data.startswith("alert_projects"))
async def interviews_projects_hr_alert(call: types.CallbackQuery):
    current_page = call.data.split(":")[1]
    await call.answer(
        text=f"Siz {current_page} - sahifadasiz", show_alert=True
    )


@interviews_projects.callback_query(F.data.startswith("next_projects:"))
async def interviews_projects_hr_next(call: types.CallbackQuery):
    await call.answer(
        cache_time=0
    )
    current_page = int(call.data.split(':')[1])
    all_pages = int(call.data.split(':')[2])

    if current_page == all_pages:
        current_page = 1
    else:
        current_page += 1

    all_projects = await db.select_projects()
    extract = extracter(
        all_medias=all_projects, delimiter=10
    )
    await prev_next_projects_func(
        extract=extract, call=call, current_page=current_page, all_pages=all_pages
    )


@interviews_projects.message(F.text == "⬅️ Ortga")
async def back_to_projects_main(message: types.Message):
    await interviews_projects_hr_one(
        message=message
    )
