from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

interviews_cbuttons = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🎙 Suhbat va loyihalar")
        ],
        [
            KeyboardButton(text="🏡 Bosh sahifa")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
