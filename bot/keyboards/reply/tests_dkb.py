from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

tests_main_dkb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Yaxin Mendelevich so'rovnomasi"),
            KeyboardButton(text="Ayzenk | Temperament aniqlash")
        ],
        [
            KeyboardButton(text="Leongard so'rovnomasi")
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
