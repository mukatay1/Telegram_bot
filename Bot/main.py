import asyncio
import os
import sys
import time

import requests

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from const import token

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class FSMInputClient(StatesGroup):
    name = State()
    time_to_exit = State()
    rating = State()


@dp.message_handler(commands="start")
async def start(message: types.Message):
    data = {
        'username': message.from_user.full_name,
        'user_id': message.from_user.id,
        'active': True

    }
    requests.post(
        'http://127.0.0.1:8000/clients/',
        data=data
    )
    buttons = ["Я Медик", "Заполнить карточку МОП"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)
    await message.answer("Вас приветствует бот Поиск Медика! Если вы медик ,не забудьте записаться",
                         reply_markup=keyboard)


@dp.message_handler(Text(equals="Заполнить карточку МОП"))
async def client_card(message: types.Message):
    await message.answer('Опишите что у вас болит')
    await FSMInputClient.name.set()


@dp.message_handler(Text(equals="Я Медик"))
async def client_card(message: types.Message):
    data = {
        'id_doctor': True
    }
    users = requests.get(
        'http://127.0.0.1:8000/clients/'
    )

    user_id = None
    for i in users.json():
        if i['user_id'] == message.from_user.id:
            user_id = i['id']
            break

    requests.patch(
        f'http://127.0.0.1:8000/clients/{user_id}/',
        data=data
    )
    await message.reply('Вы записаны как медик!')


@dp.message_handler(state=FSMInputClient.name)
async def set_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    clients_lst = requests.get(
        'http://127.0.0.1:8000/clients/'
    )
    user_id = None
    for i in clients_lst.json():
        if i['user_id'] == message.from_user.id:
            user_id = i['id']
            break

    data = {
        'user_id': user_id,
        'message': data['name'],
        'finished': False,
        'maker_id': None,
        'active': True,
        'time_to_exit': ''

    }
    requests.post(
        'http://127.0.0.1:8000/messages/',
        data=data
    )

    await message.reply('Ищем свободного медика')
    await FSMInputClient.next()
    os.execv(sys.executable, ['python'] + sys.argv)


@dp.message_handler(state=FSMInputClient.time_to_exit)
async def set_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['time_to_exit'] = message.text

    new_data = {
        'time_to_exit': data['time_to_exit']
    }

    per = requests.get(
        f'http://127.0.0.1:8000/clients/?user_id={message.from_user.id}'
    )

    k = requests.get(
        f'http://127.0.0.1:8000/messages/?maker_id={per.json()[0]["id"]}&finished=false&active=false',
    )

    requests.patch(
        f'http://127.0.0.1:8000/messages/{k.json()[0]["id"]}/',
        data=new_data
    )
    time.sleep(3)
    await message.answer('Выезжайте на адрес.Через час будет задан вопрос')
    keyboard2 = types.InlineKeyboardMarkup(row_width=2)
    btn_1 = types.InlineKeyboardButton(text='Да', callback_data='second')
    btn_2 = types.InlineKeyboardButton(text='Нет', callback_data='work')
    keyboard2.add(btn_1, btn_2)
    await bot.send_message(message.from_user.id, 'Вы приехали на адрес?', reply_markup=keyboard2)
    await FSMInputClient.next()
    os.execv(sys.executable, ['python'] + sys.argv)


func = lambda call: call.data == "second"


@dp.callback_query_handler(func)
async def call_second_yes(callback: types.CallbackQuery):
    # per = requests.get(
    #     f'http://127.0.0.1:8000/clients/?user_id={callback["from"]["id"]}'
    # )
    # mes = requests.get(
    #     f'http://127.0.0.1:8000/messages/?user_id={per.json()[0]["id"]}&message={callback["message"]["text"].replace("-Откликнуться?", "")}'
    # )
    # await asyncio.sleep(3)
    keyboard3 = types.InlineKeyboardMarkup(row_width=2)
    btn_3 = types.InlineKeyboardButton(text='Да', callback_data='third')
    btn_4 = types.InlineKeyboardButton(text='Нет', url='facebook.com')
    keyboard3.add(btn_3, btn_4)
    await callback.message.answer('Вы услугу оказали?', reply_markup=keyboard3)
    os.execv(sys.executable, ['python'] + sys.argv)


func1 = lambda call: call.data == "third"


@dp.callback_query_handler(func1)
async def call_third_yes(callback: types.CallbackQuery):
    await callback.message.answer('Заплатите за услугу')
    per = requests.get(
        f'http://127.0.0.1:8000/clients/?user_id={callback["from"]["id"]}'
    )
    mes = requests.get(
        f'http://127.0.0.1:8000/messages/?user_id={per.json()[0]["id"]}&active=false&finished&false'
    )

    data = {
        'finished': True,
    }
    requests.patch(
        f'http://127.0.0.1:8000/messages/{mes.json()[0]["id"]}/',
        data=data
    )
    await callback.message.answer('Оцените услугу медика  от 1 до 10')
    await FSMInputClient.rating.set()


@dp.message_handler()
async def ask_about_client(self):
    while True:
        new_order = requests.get(
            'http://127.0.0.1:8000/clients/?id_doctor=true'  # active=true
        )
        lst = requests.get(
            'http://127.0.0.1:8000/messages/?finished=false&active=true'
        )
        for i in new_order.json():
            for j in lst.json():
                keyboard1 = types.InlineKeyboardMarkup(row_width=2)
                btn1 = types.InlineKeyboardButton(text='Да ', callback_data='yes')
                btn2 = types.InlineKeyboardButton(text='Нет', url='facebook.com')
                keyboard1.add(btn1, btn2)
                await bot.send_message(i['user_id'], f"{j['data_created']}")
                await bot.send_message(i['user_id'], f"{j['message']}-Откликнуться?",
                                       reply_markup=keyboard1)

        await asyncio.sleep(30)


@dp.callback_query_handler(text='yes')
async def call_yes(callback: types.CallbackQuery):
    per = requests.get(
        f'http://127.0.0.1:8000/clients/?user_id={callback["from"]["id"]}'
    )

    data = {
        'active': False
    }
    requests.patch(
        f'http://127.0.0.1:8000/clients/{per.json()[0]["id"]}/',
        data=data
    )

    mes = requests.get(
        f'http://127.0.0.1:8000/messages/?user_id={per.json()[0]["id"]}&message={callback["message"]["text"].replace("-Откликнуться?", "")}'
    )

    new_data = {
        'active': False,
        'maker_id': per.json()[0]["id"]
    }
    requests.patch(
        f'http://127.0.0.1:8000/messages/{mes.json()[0]["id"]}/',
        data=new_data
    )

    await callback.message.answer('Через какое время можете быть на месте?')
    await bot.send_message(per.json()[0]["user_id"], 'Медик назначен')
    await callback.answer()
    await FSMInputClient.time_to_exit.set()


@dp.message_handler(state=FSMInputClient.rating)
async def set_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['rating'] = message.text

    new_data = {
        'rating': data['rating']
    }

    per = requests.get(
        f'http://127.0.0.1:8000/clients/?user_id={message.from_user.id}'
    )

    k = requests.get(
        f'http://127.0.0.1:8000/messages/?maker_id={per.json()[0]["id"]}&finished=true&active=false',
    )

    requests.patch(
        f'http://127.0.0.1:8000/messages/{k.json()[0]["id"]}/',
        data=new_data
    )
    await message.answer('End/')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(ask_about_client(30))
    executor.start_polling(dp, skip_updates=True)
