import aiogram.exceptions
from aiogram import Router, F, types

from bot.handlers.functions.functions_one import extracter
from bot.keyboards.inline.buttons import key_returner_articles
from data.jsonfiles import articlesjson
from loader import db

articles = Router()


async def prev_next_articles_func(extracted_articles, call: types.CallbackQuery, current_page, all_pages):
    articles_ = str()

    for n in extracted_articles:
        articles_ += f"{n['id']}. <a href='{n['link']}'>{n['file_name']}</a>\n"

    try:
        await call.message.edit_text(
            text=articles_, reply_markup=key_returner_articles(
                current_page=current_page, all_pages=all_pages
            ), disable_web_page_preview=True
        )
        await call.answer(
            cache_time=0
        )
    except aiogram.exceptions.TelegramBadRequest:
        await call.answer(
            text="Boshqa sahifa mavjud emas!", show_alert=True
        )


@articles.message(F.text == "📝 Maqolalar")
async def articles_hr_one(message: types.Message):
    all_articles = await db.select_all_articles()
    if all_articles:
        extract = extracter(all_medias=all_articles, delimiter=10)
        current_page = 1
        all_pages = len(extract)

        extracted_articles = extract[current_page - 1]
        articles_ = str()

        for n in extracted_articles:
            articles_ += f"{n['id']}. <a href='{n['link']}'>{n['file_name']}</a>\n"

        await message.answer(
            text=articles_, reply_markup=key_returner_articles(
                current_page=current_page, all_pages=all_pages
            ), disable_web_page_preview=True
        )
    else:
        await message.answer(
            text="Maqolalar hozircha botga yuklanmadi"
        )


@articles.callback_query(F.data.startswith("prev_articles"))
async def articles_hr_prev(call: types.CallbackQuery):
    all_articles = await db.select_all_articles()
    extract = extracter(
        all_medias=all_articles, delimiter=10
    )
    current_page = int(call.data.split(":")[1])
    all_pages = len(extract)

    if current_page == 1:
        current_page = all_pages
    else:
        current_page -= 1

    extracted_articles = extract[current_page - 1]
    await prev_next_articles_func(
        extracted_articles=extracted_articles, call=call, current_page=current_page, all_pages=all_pages
    )


@articles.callback_query(F.data.startswith("alertarticles"))
async def articles_hr_alert(call: types.CallbackQuery):
    current_page = call.data.split(":")[1]
    await call.answer(
        text=f"Siz {current_page} - sahifadasiz", show_alert=True
    )


@articles.callback_query(F.data.startswith("next_articles"))
async def articles_hr_next(call: types.CallbackQuery):
    all_articles = await db.select_all_articles()
    extract = extracter(
        all_medias=all_articles, delimiter=10
    )
    current_page = int(call.data.split(":")[1])
    all_pages = len(extract)

    if current_page == all_pages:
        current_page = 1
    else:
        current_page += 1

    extracted_articles = extract[current_page - 1]
    await prev_next_articles_func(
        extracted_articles=extracted_articles, call=call, current_page=current_page, all_pages=all_pages
    )


@articles.message(F.text == "addarticles")
async def add_articles_handler(message: types.Message):
    c = 0
    for n in articlesjson:
        c += 1
        await db.add_articles(
            file_name=n['file_name'],
            link=n['link']
        )
    await message.answer(
        text=f"{c} ta maqola qo'shildi"
    )
