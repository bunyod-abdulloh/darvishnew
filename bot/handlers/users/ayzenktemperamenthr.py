import asyncio
import os

import aiogram
from aiogram.exceptions import TelegramBadRequest
from aiogram import Router, F, types
from matplotlib import pyplot as plt

from bot.keyboards.inline.testskb import start_test, ayzenktemp_ikb, test_link_ibutton
from bot.keyboards.reply.tests_dkb import tests_main_dkb
from loader import db

router = Router()


async def sendayztempphoto(call: types.CallbackQuery):
    telegram_id = call.from_user.id
    link = "https://telegra.ph/Ajzenk-SHahsiyat-s%D1%9Erovnomasiga-izo%D2%B3-07-20"

    lie_yes = await db.select_sum_ayztemptempyes(
        telegram_id=telegram_id, scale_type="yolgon",
    )
    lie_no = await db.select_sum_ayztemptempno(
        telegram_id=telegram_id, scale_type="yolgon",
    )

    lie = 0

    if lie_yes['sum']:
        lie += lie_yes['sum']
    if lie_no['sum']:
        lie += lie_no['sum']

    extra_intro_yes = await db.select_sum_ayztemptempyes(
        telegram_id=telegram_id, scale_type="extra-intro",
    )
    extra_intro_no = await db.select_sum_ayztemptempno(
        telegram_id=telegram_id, scale_type="extra-intro",
    )
    neuro = await db.select_sum_ayztemptempyes(
        telegram_id=telegram_id, scale_type="neyrotizm"
    )

    x = 0
    y = 0

    if extra_intro_yes['sum']:
        x += extra_intro_yes['sum']
    elif extra_intro_no['sum']:
        x += extra_intro_no['sum']

    if neuro['sum']:
        y += neuro['sum']

    extroversion = float(x)
    neuroticism = float(y)

    if 12 in (extroversion, neuroticism):
        await call.message.edit_text(
            text="Кўрсаткичларингиз иккита темпераментга тўғри келиб қолди, сўровномага "
                 "қайта жавоб беришингиз лозим!"
        )
    elif lie > 4:
        await call.message.edit_text(
            text="Ёлғон мезони бўйича натижангиз 4 баллдан ошиб кетди! Сўровномага қайта жавоб беришингиз лозим!"
        )
    else:
        await call.message.edit_text(
            text="Сўровнома якунланди!\n\n"
                 "Натижани суратдан юклаб олинг!"
        )

    await asyncio.sleep(3)

    temperament = str()

    if extroversion > 12 < neuroticism:
        temperament = (f"Темперамент: Холерик"
                       f"\n\nЭкстраверсия - интроверсия: {extroversion} балл"
                       f"\n\nНейротизм: {neuroticism} балл")

    if extroversion > 12 > neuroticism:
        temperament = (f"Темперамент: Сангвиник"
                       f"\n\nЭкстраверсия - интроверсия: {extroversion} балл"
                       f"\n\nНейротизм: {neuroticism} балл")

    if extroversion < 12 > neuroticism:
        temperament = (f"Темперамент: Флегматик"
                       f"\n\nЭкстраверсия - интроверсия: {extroversion} балл"
                       f"\n\nНейротизм: {neuroticism} балл")

    if extroversion < 12 < neuroticism:
        temperament = (f"Темперамент: Меланхолик"
                       f"\n\nЭкстраверсия - интроверсия: {extroversion} балл"
                       f"\n\nНейротизм: {neuroticism} балл")

    # Chizma
    plt.figure(figsize=(10, 15))
    plt.xlim(0, 24)
    plt.ylim(0, 24)

    # O'qlar va markaz
    plt.axhline(12, color='gray', linestyle='--')
    plt.axvline(12, color='gray', linestyle='--')

    # Ko'rsatkich nuqtasi
    plt.scatter(extroversion, neuroticism, color='red', s=100)
    plt.text(extroversion + 0.5, neuroticism, f'({extroversion}, {neuroticism})', fontsize=12)

    plt.figtext(0.5, 0.90, f'Сизнинг кўрсаткичларингиз:\n\n{temperament}', fontsize=12, ha='center',
                bbox=dict(facecolor='white', alpha=0.5), linespacing=0.7)
    # Orqa fon matni
    plt.text(12, 12, '@gavhardarvish_bot', fontsize=60, color='grey', alpha=0.2, ha='center',
             va='center', rotation=60)

    # Har bir temperament turiga xos xususiyatlar
    plt.text(14, 20, 'Холерик:\nЭкстраверт, Актив, Эмоционал', fontsize=10,
             bbox=dict(facecolor='white', alpha=0.1))
    plt.text(14, 4, 'Сангвиник:\nЭкстраверт, Оптимист, Ижтимоий', fontsize=10,
             bbox=dict(facecolor='white', alpha=0.1))
    plt.text(2, 4, 'Флегматик:\nИнтроверт, Тинч, Барқарор', fontsize=10,
             bbox=dict(facecolor='white', alpha=0.1))
    plt.text(2, 20, 'Меланхолик:\nИнтроверт, Ҳиссий, Ташвишли', fontsize=10,
             bbox=dict(facecolor='white', alpha=0.1))

    # O'qlardagi raqamlar
    plt.xticks(range(0, 25, 2))
    plt.yticks(range(0, 25, 2))

    plt.xlabel('Экстраверсия')
    plt.ylabel('Нейротизм')

    plt.grid(True)

    # Rasmni saqlash
    plt.savefig(f'{telegram_id}.png')
    user = await db.select_user(
        telegram_id=telegram_id
    )
    await call.message.answer_photo(
        photo=types.input_file.FSInputFile(f"{telegram_id}.png"), caption=f"Тест тури: Айзенк | Шахсият сўровномаси\n\n"
                                                                          f"Ф.И.О: {user['fio']}\n\n"
                                                                          f"Телефон рақам: {user['phone']}\n\n",
        reply_markup=test_link_ibutton(link=link)
    )
    os.remove(f"{telegram_id}.png")
    await db.delete_ayztemptemp(
        telegram_id=telegram_id
    )


async def ayztemplastquestion(question_id: int, call: types.CallbackQuery):
    if question_id == 57:
        await sendayztempphoto(
            call=call
        )
    else:
        all_questions = await db.select_questions_ayztemp()
        try:
            await call.message.edit_text(
                text=f"{all_questions[question_id]['question_number']} / {len(all_questions)}\n\n"
                     f"{all_questions[question_id]['question']}",
                reply_markup=ayzenktemp_ikb(
                    testdb=all_questions[question_id]
                )
            )
        except aiogram.exceptions.TelegramBadRequest:
            await call.answer(
                text="Server bilan aloqa yaxshi emas! Iltimos tugmani faqat bir marta bosing!", show_alert=True
            )


@router.message(F.text == "Ayzenk | Temperament aniqlash")
async def temperament_router(message: types.Message):
    await db.delete_ayztemptemp(
        telegram_id=message.from_user.id
    )
    # await message.answer(
    #     text="Техник ишлар амалга оширилмоқда! Техник ишлар якунлангач сўровномани қайта ишлашингизни сўраймиз."
    # )
    await message.answer(
        text="Айзенкнинг <b>Шахсият сўровномаси</b> 57 та саволдан иборат. Жавоблар 3 та мезон"
             "(интроверсия/экстраверсия, нейротизм ва ёлғон)лар асосида таҳлил қилиниб натижа чиқарилади. Сўровнома "
             "Сиздаги доминант темпераментни аниқлашга ёрдам беради. Саволларнинг 24 таси шахснинг интроверт ёки "
             "экстраверт эканлигини аниқлашга, 24 таси шахснинг ҳиссий барқарор ёки барқарор эмаслигини "
             "аниқлаш(нейротизм)га ва қолган 9 таси сўровнома тўлдирувчи шахснинг сўровномага муносабатини аниқлашга "
             "қаратилган."
             "\n\nСиз саволларни ўқиб, уларга жавоб беришингиз лозим. Уларга “Ҳа” ёки “Йўқ” деб жавоб беринг, "
             "ҳаёлингизга келган биринчи жавобни ёзинг, улар устида узоқ ўйлаб ўтирманг, чунки жавобни аниқлашга "
             "дастлабки реакциянгиз муҳим. Тўғри ва нотўғри жавобнинг ўзи йўқ, бу ерда бор-йўғи шахсингиз аниқланади "
             "холос."
             "\n\nСўровнома якунлангач, интроверт ёки экстраверт эканлигингиз, нейротизм даражаси ва қайси темперамент "
             "доминант эканлиги кўрсатилади."
             "\n\n<b><i>Эслатма:\n\nЁлғон мезони бўйича кўрсаткичингиз 4 баллдан ошиб кетса ёки "
             "натижа сифатида иккита темперамент чиқарилса сўровномани қайта ишлашингиз лозим!</i></b>",
        reply_markup=start_test(
            callback="ayztemp"
        )
    )


@router.callback_query(F.data == "ayztemp")
async def ayztemp_go(call: types.CallbackQuery):
    await db.delete_ayztemptemp(
        telegram_id=call.from_user.id
    )
    all_questions = await db.select_questions_ayztemp()

    await call.message.edit_text(
        text=f"{all_questions[0]['question_number']} / {len(all_questions)}\n\n{all_questions[0]['question']}",
        reply_markup=ayzenktemp_ikb(
            testdb=all_questions[0]
        )
    )


@router.callback_query(F.data.startswith("ayztempyes:"))
async def ayzyes_callback(call: types.CallbackQuery):
    question_id = int(call.data.split(":")[1])
    telegram_id = call.from_user.id
    await call.answer(
        cache_time=0
    )

    get_yes = await db.get_yes_ayzscales(
        yes=question_id
    )
    if get_yes:
        get_question = await db.select_check_ayztemptemp(
            telegram_id=telegram_id, question_number=question_id
        )
        if get_question is None:
            await db.add_ayztemptempyes(
                telegram_id=telegram_id, scale_type=get_yes['scale_type'], question_number=question_id, yes=1
            )
    await ayztemplastquestion(
        question_id=question_id, call=call
    )


@router.callback_query(F.data.startswith("ayztempno:"))
async def ayzno_callback(call: types.CallbackQuery):
    question_id = int(call.data.split(":")[1])
    telegram_id = call.from_user.id
    await call.answer(
        cache_time=0
    )
    get_no = await db.get_no_ayzscales(
        no_=question_id
    )

    if get_no:
        get_question = await db.select_check_ayztemptemp(
            telegram_id=telegram_id, question_number=question_id
        )
        if get_question is None:
            await db.add_ayztemptempno(
                telegram_id=telegram_id, scale_type=get_no['scale_type'], question_number=question_id, no_=1
            )
    await ayztemplastquestion(
        question_id=question_id, call=call
    )


@router.callback_query(F.data.startswith("ayztempback"))
async def ayzback_callback(call: types.CallbackQuery):
    question_id = int(call.data.split(":")[1])
    telegram_id = call.from_user.id

    if question_id == 0:
        await call.message.delete()
        await call.message.answer(
            text="🧑‍💻 Testlar | So'rovnomalar", reply_markup=tests_main_dkb
        )
    else:
        await db.back_user_ayztemptemp(
            telegram_id=telegram_id, question_number=question_id
        )

        all_questions = await db.select_questions_ayztemp()

        await call.message.edit_text(
            text=f"{all_questions[question_id - 1]['question_number']} / {len(all_questions)}"
                 f"\n\n{all_questions[question_id - 1]['question']}",
            reply_markup=ayzenktemp_ikb(
                testdb=all_questions[question_id - 1]
            )
        )
