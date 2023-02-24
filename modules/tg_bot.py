import asyncio

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from misc import bot_content
from app import secure_data
from misc.states import NormalMode, Predict
from modules.openai_api import make_openai_request

API_TOKEN = secure_data.TELEGRAM_API_KEY

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    photo = open(file="img.png", mode="rb")
    await bot.send_photo(
        chat_id=message.chat.id, photo=photo, caption=bot_content.bot_info
    )
    return await welcome_command(message)


async def delete_previous_messages(chat_id: int, message_ids: list[int]):
    for i in message_ids:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=i)
        except:
            pass


@dp.message_handler(lambda message: message.text == bot_content.back_to_menu_button.text, state="*")
async def back_to_menu_command(message: types.Message, state: FSMContext):
    await state.finish()
    await delete_previous_messages(
        chat_id=message.chat.id,
        message_ids=[message.message_id, message.message_id - 1],
    )
    await welcome_command(message=message)


@dp.callback_query_handler(lambda call: call.data == bot_content.back_to_menu_callback_button.callback_data, state='*')
async def back_to_menu_callback_command(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await delete_previous_messages(
        chat_id=call.message.chat.id,
        message_ids=[call.message.message_id]
    )
    await welcome_command(message=call.message)


@dp.message_handler()
async def welcome_command(message: types.Message):
    await message.answer(
        text=bot_content.hi_message, reply_markup=bot_content.mode_keyboard()
    )


@dp.callback_query_handler(lambda call: call.data == bot_content.predict_button.callback_data)
async def predict_command(call: types.CallbackQuery):
    await delete_previous_messages(
        chat_id=call.message.chat.id,
        message_ids=[call.message.message_id, call.message.message_id - 2],
    )
    await call.message.answer(
        text=bot_content.predict_message, reply_markup=bot_content.sport_keyboard
    )


@dp.callback_query_handler(lambda call: call.data == bot_content.normal_mode_button.callback_data)
async def normal_mode_command(call: types.CallbackQuery):
    await delete_previous_messages(
        chat_id=call.message.chat.id,
        message_ids=[call.message.message_id, call.message.message_id - 2],
    )
    await call.message.answer(
        text=bot_content.normal_mode_message,
        reply_markup=bot_content.back_to_menu_keyboard(),
    )
    await NormalMode.question.set()


@dp.message_handler(state=NormalMode.question)
async def get_info_normal_mode_command(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(bot_content.please_wait_message)
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, make_openai_request, message.text.strip())
    await message.answer(f"Запрос: {message.text}\n\nОтвет: " + response)
    await delete_previous_messages(chat_id=message.chat.id,
                                   message_ids=[message.message_id + 1, message.message_id, message.message_id - 1])
    return await welcome_command(message)


@dp.callback_query_handler(lambda call: call.data in bot_content.sport_types.keys(), state='*')
async def get_sport_type_command(call: types.CallbackQuery, state: FSMContext):
    await call.answer(f"Выбран спорт: {call.data}")
    await delete_previous_messages(chat_id=call.message.chat.id, message_ids=[call.message.message_id])
    await call.message.answer(bot_content.choose_commands_message,
                              reply_markup=bot_content.back_to_menu_keyboard())
    async with state.proxy() as data:
        data["sport_type"] = call.data
    await Predict.commands_names.set()


@dp.message_handler(state=Predict.commands_names)
async def get_commands_names_command(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["commands_names"] = message.text
    await message.answer(bot_content.choose_date_message, reply_markup=bot_content.back_to_menu_keyboard())
    await Predict.date.set()


@dp.message_handler(state=Predict.date)
async def get_info_predict_mode_command(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        information = data.as_dict()
    sport_type = information['sport_type']
    commands_names = information['commands_names']
    date = message.text.strip()
    question = f"Выдай пример прогноза на это событие: Тип спорта: {sport_type}" \
               f" Участники: {commands_names} Дата: {date}" \
               f"Главное: Пиши только на русском языке с правильными формами слов, обязательно овтеть на все вопросы! В ответе распиши эти параметры: {bot_content.sport_types[sport_type]}. Напиши по пунктам ответы максммально кратко, без лишней информации, каждый ответ пиши в формате Вопрос: Ответ. Каждый ответ должен быть с новой строки. В самом начале своего сообщения упомяни тип спорта, дату и команды."
    await state.finish()
    await message.answer(bot_content.please_wait_message)
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, make_openai_request, question)
    await message.answer(f"Запрос: {sport_type}, {commands_names}, {date}\n\nОтвет: "
                         + response)
    await delete_previous_messages(chat_id=message.chat.id,
                                   message_ids=[message.message_id + 1, message.message_id, message.message_id - 1,
                                                message.message_id - 2, message.message_id - 3])
    return await welcome_command(message)


executor.start_polling(dp, skip_updates=True)
