from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

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
            KeyboardButton(text="📝 Maqolalar")
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Habaringizni kiriting...",
    one_time_keyboard=True
)
