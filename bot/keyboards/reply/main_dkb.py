from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo

main_dkb = ReplyKeyboardMarkup(
    keyboard=
    [
        [
            KeyboardButton(text="🧑‍💻 Testlar | So'rovnomalar")
        ],
        [
            KeyboardButton(text="📚 Kurslar"),
            KeyboardButton(text="🎙 Suhbat va loyihalar")
        ],
        [
            KeyboardButton(text="📝 Maqolalar"),
            KeyboardButton(text="📲 Adminga murojaat", web_app=WebAppInfo(
                url="https://t.me/Hidaya_academy_administrator"
            ))
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Habaringizni kiriting...",
    one_time_keyboard=True
)
