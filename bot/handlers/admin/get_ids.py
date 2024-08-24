from aiogram import F, types, Router

from bot.filters import IsBotAdminFilter
from data.config import ADMINS
from loader import db

router = Router()


@router.message(IsBotAdminFilter(ADMINS), F.media_group_id)
async def handle_albums(message: types.Message, album: types.List[types.Message]):
    """This handler will receive a complete album of any type."""
    group_elements = []

    for element in album:
        caption_kwargs = {"caption": element.caption, "caption_entities": element.caption_entities}

        if element.photo:
            input_media = types.InputMediaPhoto(media=element.photo[-1].file_id, **caption_kwargs)

        elif element.video:
            input_media = types.InputMediaVideo(media=element.video.file_id, **caption_kwargs)
        elif element.document:
            input_media = types.InputMediaDocument(media=element.document.file_id, **caption_kwargs)
        elif element.audio:
            input_media = types.InputMediaAudio(media=element.audio.file_id, **caption_kwargs)
        else:
            return message.answer("This media type isn't supported!")

        group_elements.append(input_media)

    return message.answer_media_group(group_elements)


@router.message(IsBotAdminFilter(ADMINS), F.photo)
async def get_photo_id(message: types.Message):
    photo_id = message.photo[-1].file_id
    await message.answer(
        text=f"Photo ID: <code>{photo_id}</code>"
    )


@router.message(IsBotAdminFilter(ADMINS), F.audio)
async def get_audio_id(message: types.Message):
    audio_id = message.audio.file_id
    caption = message.caption
    await db.add_projects(
        category="category",
        subcategory="subcategory",
        sequence=1,
        file_type='audio',
        file_id=audio_id,
        caption=caption
    )
    await message.answer(
        text=f"Audio databasega joylandi!"
    )


@router.message(IsBotAdminFilter(ADMINS), F.video)
async def get_video_id(message: types.Message):
    video_id = message.video.file_id
    caption = message.caption
    await db.add_projects(
        category="category",
        subcategory="subcategory",
        sequence=1,
        file_type='video',
        file_id=video_id,
        caption=caption
    )
    await message.answer(
        text=f"Videolar databasega joylandi!"
    )


@router.message(IsBotAdminFilter(ADMINS), F.document)
async def get_document_id(message: types.Message):
    document_id = message.document.file_id
    caption = message.caption
    await message.answer(
        text=f"Document ID: <code>{document_id}</code>"
    )
