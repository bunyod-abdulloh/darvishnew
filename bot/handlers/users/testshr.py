import os

import aiogram
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from bot.keyboards.inline.testskb import test_ibuttons, start_test
from bot.keyboards.reply.tests_dkb import tests_main_dkb
from bot.states.userstates import UserAnketa
from loader import db

test = Router()


@test.message(F.text == "🧑‍💻 Testlar | So'rovnomalar")
async def tests_main_hr(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    user = await db.select_user(
        telegram_id=telegram_id
    )
    if user['fio']:
        await message.answer(
            text="🧑‍💻 Testlar | So'rovnomalar", reply_markup=tests_main_dkb
        )
    else:
        await message.answer(
            text="Фамилия, исм ва отангизни исмини киритинг:\n\n"
                 "<b>(Намуна: Тешабаева Гавҳар Дарвишовна)</b>"
        )
        await state.set_state(
            state=UserAnketa.addfullname
        )


@test.message(UserAnketa.addfullname)
async def addfullname(message: types.Message, state: FSMContext):
    await db.updateuser_fullname(
        telegram_id=message.from_user.id, fio=message.text
    )
    await message.answer(
        text="Телефон рақамингизни киритинг:\n\n"
             "<b>(Намуна: +998991234567)</b>"
    )
    await state.set_state(UserAnketa.addphone)


@test.message(UserAnketa.addphone)
async def addphone(message: types.Message, state: FSMContext):
    await db.updateuser_phone(
        telegram_id=message.from_user.id, phone=message.text
    )
    await message.answer(
        text="🧑‍💻 Testlar | So'rovnomalar", reply_markup=tests_main_dkb
    )
    await state.clear()


@test.message(F.text == "Yaxin Mendelevich so'rovnomasi")
async def test_command(message: types.Message):
    telegram_id = message.from_user.id
    await db.delete_user_yaxintemporary(
        telegram_id=telegram_id
    )
    await message.answer(
        text="Ушбу клиник сўровнома невротик ҳолатларнинг асосий синдромларини аниқлашга ёрдам беради. "
             "Клиник сўровнома натижалари қуйидаги 6 та мезон бўйича аниқланиб таҳлил қилинади:\n\n1) Хавотир мезони "
             "\n2) Невротик депрессия мезони \n3) Астения мезони\n4) Истерик тоифадаги жавоб мезони "
             "\n5) Обсессив - фобик бузилишлар мезони\n6) Вегетатив бузилишлар мезони"
             "\n\n<b>Йўриқнома:</b>\n\nХозирги ҳолатингизни тасвирловчи 68 та саволлар тўпламига қуйидаги 5 та "
             "жавобдан бирини танлаб жавоб беришингиз лозим:  \n • Ҳеч қачон \n • Камдан - кам \n • Баъзида "
             "\n • Тез - тез \n • Доим "
             "\n\nСўровнома якунлангач ҳар бир мезон бўйича кўрсаткичларингиз тақдим этилади.",
        reply_markup=start_test(
            callback="yaxintest"
        )
    )


@test.callback_query(F.data == "yaxintest")
async def start_test_yaxin(call: types.CallbackQuery):
    all_questions = await db.select_all_yaxin()
    await call.message.edit_text(
        text=f"{all_questions[0]['id']} / {len(all_questions)}\n\n{all_questions[0]['question']}",
        reply_markup=test_ibuttons(
            testdb=all_questions[0]
        ))


@test.callback_query(F.data.startswith("point_"))
async def test_callback(call: types.CallbackQuery):
    column_name = call.data.split(":")[0]
    scale_type = call.data.split(":")[1]
    question_number = int(call.data.split(":")[2])
    telegram_id = call.from_user.id
    await call.answer(
        cache_time=0
    )

    all_questions = await db.select_all_yaxin()

    if "-" in scale_type:
        scale_one = scale_type.split("-")[0]
        scale_two = scale_type.split("-")[1]
        point_one = await db.select_question_scale(
            scale_type=scale_one, question_number=question_number
        )
        point_two = await db.select_question_scale(
            scale_type=scale_two, question_number=question_number
        )
        await db.add_yaxin_temporary(
            telegram_id=telegram_id, scale_type=scale_one, question_number=question_number,
            test_type="nevroz_yaxin", answer=point_one[column_name]
        )
        await db.add_yaxin_temporary(
            telegram_id=telegram_id, scale_type=scale_two, question_number=question_number,
            test_type="nevroz_yaxin", answer=point_two[column_name]
        )
    else:
        point = await db.select_question_scale(
            scale_type=scale_type, question_number=question_number
        )
        await db.add_yaxin_temporary(
            telegram_id=telegram_id, scale_type=scale_type, question_number=question_number,
            test_type="nevroz_yaxin", answer=point[column_name]
        )

    if all_questions[-1]['id'] == question_number:
        xavotir = await db.select_datas_temporary(
            telegram_id=telegram_id, scale_type="xavotir"
        )
        nevrotik_depressiya = await db.select_datas_temporary(
            telegram_id=telegram_id, scale_type="nevrotikdep"
        )
        asteniya = await db.select_datas_temporary(
            telegram_id=telegram_id, scale_type="astenik"
        )
        isterik = await db.select_datas_temporary(
            telegram_id=telegram_id, scale_type="isterik"
        )
        obsessivfobik = await db.select_datas_temporary(
            telegram_id=telegram_id, scale_type="obsessivfobik"
        )
        vegetativ = await db.select_datas_temporary(
            telegram_id=telegram_id, scale_type="vegetativ"
        )

        result = [xavotir, nevrotik_depressiya, asteniya, isterik, obsessivfobik, vegetativ]

        text = str()

        if any(number < -1.28 for number in result):
            text += "Невротик ҳолат мавжуд!"
        else:
            text += "Невротик ҳолат мавжуд эмас!"
        user = await db.select_user(
            telegram_id=telegram_id
        )
        photo = f"Тест тури: Яхин, Менделевич | Невротик ҳолатни аниқлаш\n\n" \
                f"Ф.И.О: {user['fio']}\n\n" \
                f"Телефон рақам: {user['phone']}\n\n" \
                f"Xавотир мезони: {xavotir}\n\n" \
                f"Невротик-депрессия мезони: {nevrotik_depressiya}\n\n" \
                f"Астения мезони: {asteniya}\n\n" \
                f"Истерик тоифадаги жавоб мезони: {isterik}\n\n" \
                f"Обсессив-фобик бузилишлар мезони: {obsessivfobik}\n\n" \
                f"Вегетатив бузилишлар мезони: {vegetativ}\n\n{text}"

        import matplotlib.pyplot as plt

        plt.figure(figsize=(10, 5))

        # Matnni joylashtirish
        plt.text(0, 1, photo, fontsize=12, ha='left', va='top', transform=plt.gca().transAxes)

        # O'qlarni o'chirib qo'yamiz
        plt.axis('off')
        photo_link = f"{telegram_id}.png"
        # Rasmni saqlaymiz
        plt.savefig(photo_link, bbox_inches='tight', dpi=300)

        # Rasmni ko'rsatish
        plt.show()
        await call.message.delete()
        sent_message = await call.message.answer_photo(
            photo=types.input_file.FSInputFile(photo_link),
            caption=f"<b>Сўровнома якунланди!\n\n</b>"
                    f"Натижангиз кўрсаткичларини юқоридаги расмдан юклаб олишингиз мумкин!\n\n"
                    f"Мезонлардаги кўрсаткичлар + 1.28 дан юқори бўлса соғломлик даражасини, - 1.28 дан паст бўлса "
                    f"невротик ҳолат борлигидан далолат беради. Иккисини ўртасидаги кўрсаткич эса нотурғун психик "
                    f"мослашувчанликни билдиради.\n\n"
                    f"<b><i>Консультация учун:\n\n@Hidaya_Med_Clinic_administrator\n\n"
                    f"+998339513444</i></b>"
        )
        file_id = sent_message.photo[-1].file_id

        await db.delete_user_yaxintemporary(
            telegram_id=telegram_id
        )
        os.remove(photo_link)
    else:
        try:
            await call.message.edit_text(
                text=f"{all_questions[question_number]['id']} / {len(all_questions)}"
                     f"\n\n{all_questions[question_number]['question']}",
                reply_markup=test_ibuttons(
                    testdb=all_questions[question_number]
                )
            )
        except aiogram.exceptions.TelegramBadRequest:
            pass


@test.callback_query(F.data.startswith("yaxinback:"))
async def test_back_callback(call: types.CallbackQuery):
    question_number = int(call.data.split(":")[1])
    telegram_id = call.from_user.id

    if question_number == 0:
        await call.message.delete()
        await call.message.answer(
            text="🧑‍💻 Testlar | So'rovnomalar", reply_markup=tests_main_dkb
        )
    else:
        await db.back_user_yaxintemporary(
            telegram_id=telegram_id, question_number=question_number
        )

        all_questions = await db.select_all_yaxin()

        await call.message.edit_text(
            text=f"{all_questions[question_number - 1]['id']} / {len(all_questions)}"
                 f"\n\n{all_questions[question_number - 1]['question']}",
            reply_markup=test_ibuttons(
                testdb=all_questions[question_number - 1]
            )
        )
