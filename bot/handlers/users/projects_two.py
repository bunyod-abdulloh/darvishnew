import aiogram.exceptions
from aiogram import Router, F, types

from bot.handlers.functions.functions_one import extracter
from bot.keyboards.inline.buttons import interviews_first_ibuttons
from loader import db

router = Router()


async def next_prev_projects(items, items_index, call: types.CallbackQuery, markup):
    media = items[items_index]['file_id']
    caption = items[items_index]['caption']

    if items[items_index]['file_type'] == 'audio':
        await call.message.edit_media(
            media=types.InputMediaAudio(
                media=media, caption=caption
            ), reply_markup=markup
        )
    if items[items_index]['file_type'] == 'video':
        await call.message.edit_media(
            media=types.InputMediaVideo(
                media=media, caption=caption
            ), reply_markup=markup
        )


@router.callback_query(F.data.startswith("projects:"))
async def interviews_projects_hr_projects(call: types.CallbackQuery):
    category_id = int(call.data.split(":")[1])

    get_category = await db.select_project_name(
        id_=category_id
    )
    select_category = await db.select_project_by_categories(
        category_name=get_category['category']
    )

    extract = extracter(
        all_medias=select_category, delimiter=5
    )

    current_page = 1
    all_pages = len(extract)

    items = extract[current_page - 1]

    markup = interviews_first_ibuttons(
        items=items, current_page=current_page, all_pages=all_pages, selected=1
    )

    await call.message.delete()
    if items[0]['file_type'] == "audio":
        await call.message.answer_audio(
            audio=items[0]['file_id'], caption=f"{items[0]['caption']}", reply_markup=markup
        )
    if items[0]['file_type'] == "video":
        await call.message.answer_video(
            video=items[0]['file_id'], caption=f"{items[0]['caption']}", reply_markup=markup
        )


@router.callback_query(F.data.startswith("prev_pts"))
async def projects_two_prev(call: types.CallbackQuery):
    await call.answer(
        cache_time=0
    )

    current_page = int(call.data.split(":")[1])
    id_ = int(call.data.split(":")[2])

    get_category = await db.select_project_by_id(
        id_=id_
    )
    select_category = await db.select_project_by_categories(
        category_name=get_category['category']
    )

    extract = extracter(
        all_medias=select_category, delimiter=5
    )

    all_pages = len(extract)

    if current_page == 1:
        current_page = all_pages
    else:
        current_page -= 1

    items = extract[current_page - 1]

    markup = interviews_first_ibuttons(
        items=items, current_page=current_page, all_pages=all_pages, selected=items[-1]['sequence']
    )

    try:
        await next_prev_projects(
            items=items, items_index=-1, call=call, markup=markup
        )
    except aiogram.exceptions.TelegramBadRequest:
        pass


@router.callback_query(F.data.startswith("select_pts:"))
async def projects_two_two(call: types.CallbackQuery):
    await call.answer(
        cache_time=0
    )
    id_ = int(call.data.split(":")[1])
    current_page = int(call.data.split(":")[2])

    get_data = await db.select_project_by_id(
        id_=id_
    )
    select_category = await db.select_project_by_categories(
        category_name=get_data['category']
    )

    extract = extracter(
        all_medias=select_category, delimiter=5
    )

    items = extract[current_page - 1]

    markup = interviews_first_ibuttons(
        items=items, current_page=current_page, all_pages=len(extract), selected=get_data['sequence']

    )
    media = get_data['file_id']
    caption = f"{get_data['caption']}"

    try:
        if get_data['file_type'] == 'audio':
            await call.message.edit_media(
                media=types.InputMediaAudio(
                    media=media, caption=caption
                ), reply_markup=markup
            )
        if get_data['file_type'] == 'video':
            await call.message.edit_media(
                media=types.InputMediaVideo(
                    media=media, caption=caption
                ), reply_markup=markup
            )
    except aiogram.exceptions.TelegramBadRequest:
        pass


@router.callback_query(F.data.startswith("alert_pts:"))
async def projects_two_alert(call: types.CallbackQuery):
    current_page = call.data.split(":")[1]
    await call.answer(
        text=f"Siz {current_page} - sahifadasiz", show_alert=True
    )


@router.callback_query(F.data.startswith("next_pts"))
async def projects_two_next(call: types.CallbackQuery):
    await call.answer(
        cache_time=0
    )

    current_page = int(call.data.split(":")[1])
    id_ = int(call.data.split(":")[2])

    get_category = await db.select_project_by_id(
        id_=id_
    )
    select_category = await db.select_project_by_categories(
        category_name=get_category['category']
    )

    extract = extracter(
        all_medias=select_category, delimiter=5
    )

    all_pages = len(extract)

    if current_page == all_pages:
        current_page = 1
    else:
        current_page += 1

    items = extract[current_page - 1]

    markup = interviews_first_ibuttons(
        items=items, current_page=current_page, all_pages=all_pages, selected=items[0]['sequence']
    )
    # content_url = "https://telegra.ph/Hidaya-korsatuvi-10-17"
    try:
        await next_prev_projects(
            items=items, items_index=0, call=call, markup=markup
        )
    except aiogram.exceptions.TelegramBadRequest:
        pass


@router.callback_query(F.data.startswith("content_projects:"))
async def projects_two_one(call: types.CallbackQuery):
    current_page = int(call.data.split(':')[1])
    category = call.data.split(':')[2]
    get_category = await db.select_project_by_categories(
        category_name=category
    )
    extract = extracter(all_medias=get_category, delimiter=5)
    items = extract[current_page - 1]

    content = str()
    for item in items:
        content += f"{item['subcategory']}\n"

    await call.answer(
        text=content, show_alert=True
    )
