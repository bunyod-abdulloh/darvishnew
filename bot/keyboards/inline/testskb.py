from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo


def start_test(callback):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="🚀 Бошлаш", callback_data=callback)
        ]]
    )
    return markup


def test_link_ibutton(link):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="🧑‍⚕️ Кўрсатмалар", web_app=WebAppInfo(
                url=link
            ))
        ]]
    )
    return markup


# https://telegra.ph/Nevrotik-%D2%B3olat-uchun-k%D1%9Ersatmalar-07-13


def test_ibuttons(testdb):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=testdb['a'], callback_data=f"point_five:{testdb['scale_type']}:{testdb['id']}"
                ),
                InlineKeyboardButton(
                    text=testdb['b'], callback_data=f"point_four:{testdb['scale_type']}:{testdb['id']}"
                )
            ],
            [
                InlineKeyboardButton(
                    text=testdb['c'], callback_data=f"point_three:{testdb['scale_type']}:{testdb['id']}"
                ),
                InlineKeyboardButton(
                    text=testdb['d'], callback_data=f"point_two:{testdb['scale_type']}:{testdb['id']}"
                ),
                InlineKeyboardButton(
                    text=testdb['e'], callback_data=f"point_one:{testdb['scale_type']}:{testdb['id']}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Ortga", callback_data=f"yaxinback:{testdb['id'] - 1}"
                )
            ]
        ]
    )
    return markup


def ayzenktemp_ikb(testdb):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Ҳа", callback_data=f"ayztempyes:{testdb['question_number']}"
                ),
                InlineKeyboardButton(
                    text="Йўқ", callback_data=f"ayztempno:{testdb['question_number']}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Ortga", callback_data=f"ayztempback:{testdb['question_number'] - 1}"
                )
            ]
        ]
    )
    return markup


def leotest_ikb(testdb):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Ҳа", callback_data=f"leoyes:{testdb['question_number']}"
                ),
                InlineKeyboardButton(
                    text="Йўқ", callback_data=f"leono:{testdb['question_number']}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Ortga", callback_data=f"leoback:{testdb['question_number'] - 1}"
                )
            ]
        ]
    )
    return markup
