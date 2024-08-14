from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

tests_main_dkb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text="Yaxin Mendelevich so'rovnomasi"
            ),
            KeyboardButton(
                text="Ayzenk | Temperament aniqlash"
            )
        ],
        [
            KeyboardButton(
                text="Leongard so'rovnomasi"
            )
        ],
        [
            KeyboardButton(
                text="🏡 Bosh sahifa"
            )
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
