from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

interviews_cbuttons = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🎙 Suhbat va loyihalar")
        ],
        [
            KeyboardButton(text="🏡 Bosh sahifa"),
            KeyboardButton(text="📲 Adminga murojaat", web_app=WebAppInfo(
                url="https://t.me/Hidaya_academy_administrator"
            ))
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
