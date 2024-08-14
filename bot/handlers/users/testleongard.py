from aiogram import Router, F, types

from bot.keyboards.inline.testskb import leotest_ikb, start_test
from bot.keyboards.reply.tests_dkb import tests_main_dkb
from loader import db

router = Router()


async def leo_result(call: types.CallbackQuery):
    telegram_id = call.from_user.id

    isteroid_all = None
    pedantic_all = None
    rigid_all = None
    epileptoid_all = None
    gipertim_all = None
    distimic_all = None
    dangerous_all = None
    ciclomistic_all = None
    emotiv_all = None
    affectexaltir_all = None

    isteroid = await db.get_sums_leotemp(
        telegram_id=telegram_id, scale_type="isteroid"
    )
    if isteroid:
        isteroid_all = (isteroid['total_yes'] + isteroid['total_no']) * 2

    pedantic = await db.get_sums_leotemp(
        telegram_id=telegram_id, scale_type="pedantic"
    )
    if pedantic:
        pedantic_all = (pedantic['total_yes'] + pedantic['total_no']) * 2

    rigid = await db.get_sums_leotemp(
        telegram_id=telegram_id, scale_type="rigid"
    )
    if rigid:
        rigid_all = (rigid['total_yes'] + rigid['total_no']) * 2

    epileptoid = await db.get_sums_leotemp(
        telegram_id=telegram_id, scale_type="epileptoid"
    )
    if epileptoid:
        epileptoid_all = (epileptoid['total_yes'] + epileptoid['total_no']) * 3

    gipertim = await db.get_sums_leotemp(
        telegram_id=telegram_id, scale_type="gipertim"
    )
    if gipertim:
        gipertim_all = (gipertim['total_yes'] + gipertim['total_no']) * 3

    distimic = await db.get_sums_leotemp(
        telegram_id=telegram_id, scale_type="distimic"
    )
    if distimic:
        distimic_all = (distimic['total_yes'] + distimic['total_no']) * 3

    dangerous = await db.get_sums_leotemp(
        telegram_id=telegram_id, scale_type="danger"
    )
    if dangerous:
        dangerous_all = (dangerous['total_yes'] + dangerous['total_no']) * 3

    ciclomistic = await db.get_sums_leotemp(
        telegram_id=telegram_id, scale_type="ciclomistic"
    )
    if ciclomistic:
        ciclomistic_all = (ciclomistic['total_yes'] + ciclomistic['total_no']) * 3

    affectexaltir = await db.get_sums_leotemp(
        telegram_id=telegram_id, scale_type="affectexaltir"
    )
    if affectexaltir:
        affectexaltir_all = (affectexaltir['total_yes'] + affectexaltir['total_no']) * 6

    emotiv = await db.get_sums_leotemp(
        telegram_id=telegram_id, scale_type="emotiv"
    )
    if emotiv:
        emotiv_all = (emotiv['total_yes'] + emotiv['total_no']) * 3
    user = await db.select_user(
        telegram_id=telegram_id
    )
    await call.message.edit_text(
        text=f"Сўровнома якунланди!\n\n"
             f"Тест тури: Леонгард | Характерологик сўровнома"
             f"Ф.И.О: {user['fio']}\n\n"
             f"Телефон рақам: {user['phone']}\n\n"
             f"1. Намойишкор(истероид) тоифа: {isteroid_all} балл\n"
             f"2. Педантик тоифа: {pedantic_all} балл\n"
             f"3. Бир жойда қотиб қолган(ригид) тоифа: {rigid_all} балл\n"
             f"4. Тез қўзғалувчан(эпилептоид) тоифа: {epileptoid_all} балл\n"
             f"5. Гипертим тоифа: {gipertim_all} балл\n"
             f"6. Дистимик тоифа: {distimic_all} балл\n"
             f"7. Хавотирли ва қўрқувчи тоифа: {dangerous_all} балл\n"
             f"8. Циклотим тоифа: {ciclomistic_all} балл\n"
             f"9. Аффектив - экзальтир тоифа: {affectexaltir_all} балл\n"
             f"10. Эмотив тоифа: {emotiv_all} балл\n\n"
             f"Сўровнома ва шкалаларга таъриф қуйидаги ҳаволада:\n\n"
             f"https://telegra.ph/K-Leongardning-harakterologik-s%D1%9Erovnomasi-07-25"
    )
    await db.delete_leotemp(
        telegram_id=telegram_id
    )


@router.message(F.text == "Leongard so'rovnomasi")
async def leo_main_router(message: types.Message):
    await db.delete_leotemp(
        telegram_id=message.from_user.id
    )
    await message.answer(
        text="Ушбу тест характернинг акцентуациясини ўрганувчи Сўровнома бўлиб, ўз ичига 88 та савол, 10 та шкалани "
             "олади. Биринчи шкала шахсни хаётий фаоллигини ўрганувчи, иккинчи шкала эса акцентуацияни таъсирланишини "
             "намойиш этади. Учинчи шкала синалувчининг эмоционал хаётининг чуқурлигини хисобланади. Тўртинчи шкала "
             "эса синалувчининг педантизмга бўлган мойиллигини ўрганувчи хисобланади.  Бешинчи шкала юқори "
             "хавотирликни, олтинчи шкала эса кайфиятнинг сабабсиз кўтарилиб ёки аксинча тушишга бўлган мойиллигини, "
             "еттинчи шкала бўлса шахснинг намойишкорона хулқ-атворини,  саккизинчи шкаласи эса турғун турмайдиган "
             "феъл атвор,  тўққизинчи шкала чарчоқлик даражасини аниқлаш, ўнинчи эмоционал реакциясининг кучи ва ифода "
             "даражасини аниқлашга қаратилган.\nТест саволларини ечишга вақт чегараланмаган.  Биз Сиз учун, Сизни "
             "характерингизга тегишли бўлган тасдиқ саволларни хавола этамиз. Агар Сиз тасдиқ саволларга розилик "
             "берсангиз «Ҳа» тугмасини, розилик билдирмасангиз «Йўқ» тугмасини босинг. Саволлар устида кўп ўйланманг "
             "чунки тўғри ёки нотўғри жавоблар мавжуд эмас.",
        reply_markup=start_test(callback="leoxarakter")
    )


@router.callback_query(F.data == "leoxarakter")
async def leo_second_router(call: types.CallbackQuery):
    all_questions = await db.select_questions_leo()
    await call.message.edit_text(
        text=f"{all_questions[0]['question_number']} / {len(all_questions)}\n\n{all_questions[0]['question']}",
        reply_markup=leotest_ikb(all_questions[0])
    )


@router.callback_query(F.data.startswith("leoyes:"))
async def leoyes_callback(call: types.CallbackQuery):
    question_id = int(call.data.split(":")[1])
    telegram_id = call.from_user.id
    all_questions = await db.select_questions_leo()
    await call.answer(
        cache_time=0
    )

    get_yes = await db.get_yes_leoscales(
        yes=question_id
    )
    if get_yes:
        get_question = await db.select_check_leotemp(
            telegram_id=telegram_id, question_number=question_id
        )
        if get_question is None:
            await db.add_leotempyes(
                telegram_id=telegram_id, scale_type=get_yes['scale_type'], question_number=question_id, yes=1
            )
    if question_id == 88:
        await leo_result(
            call=call
        )
    else:
        await call.message.edit_text(
            text=f"{all_questions[question_id]['question_number']} / {len(all_questions)}"
                 f"\n\n{all_questions[question_id]['question']}",
            reply_markup=leotest_ikb(all_questions[question_id])
        )


@router.callback_query(F.data.startswith("leono:"))
async def leono_callback(call: types.CallbackQuery):
    question_id = int(call.data.split(":")[1])
    telegram_id = call.from_user.id
    all_questions = await db.select_questions_leo()
    await call.answer(
        cache_time=0
    )

    get_no = await db.get_no_leoscales(
        no_=question_id
    )
    if get_no:
        get_question = await db.select_check_leotemp(
            telegram_id=telegram_id, question_number=question_id
        )
        if get_question is None:
            await db.add_leotempno(
                telegram_id=telegram_id, scale_type=get_no['scale_type'], question_number=question_id, no_=1
            )
    if question_id == 88:
        await leo_result(
            call=call
        )
    else:
        await call.message.edit_text(
            text=f"{all_questions[question_id]['question_number']} / {len(all_questions)}"
                 f"\n\n{all_questions[question_id]['question']}",
            reply_markup=leotest_ikb(all_questions[question_id])
        )


@router.callback_query(F.data.startswith("leoback"))
async def leoback_callback(call: types.CallbackQuery):
    question_id = int(call.data.split(":")[1])
    telegram_id = call.from_user.id

    if question_id == 0:
        await call.message.delete()
        await call.message.answer(
            text="🧑‍💻 Testlar | So'rovnomalar", reply_markup=tests_main_dkb
        )
    else:
        await db.back_leotemp(
            telegram_id=telegram_id, question_number=question_id
        )

        all_questions = await db.select_questions_leo()

        await call.message.edit_text(
            text=f"{all_questions[question_id - 1]['question_number']} / {len(all_questions)}"
                 f"\n\n{all_questions[question_id - 1]['question']}",
            reply_markup=leotest_ikb(
                testdb=all_questions[question_id - 1]
            )
        )
