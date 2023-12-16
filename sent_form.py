from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher, Bot
import time
import datetime
from config import TOKEN_API
from keyboard import kb_start, kb_remove, check_auto_yes_and_no
from week import day_week
from data.form_data import sql_add_command, sql_add_command_check, sql_add_users

time.sleep(5)

bot = Bot(TOKEN_API)

time.sleep(5)

smauto_bot = "-1001861129956"

seconds = time.time()
result = time.localtime(seconds)
date = datetime.datetime(result.tm_year, result.tm_mon, result.tm_mday)

list_photo = []

class Auto_Data(StatesGroup):
    marka = State()
    model = State()
    year = State()
    count_photo = State()
    photo = State()
    description = State()
    address = State()
    price = State()
    name = State()
    last_name = State()
    phone_number = State()


async def auto_form_start(message: types.Message):
    await Auto_Data.marka.set()
    await message.answer("Укажите марку автомобиля", reply_markup=kb_remove)
    

async def auto_marka(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['marka'] = message.text
    await Auto_Data.next()
    await message.answer("Укажите модель автомобиля")
    

async def auto_model(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['model'] = message.text
    await Auto_Data.next()
    await message.answer("Укажите год автомобиля")


async def auto_year(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['year'] = int(message.text)
        await Auto_Data.next()
        await message.answer("Добавить можно до 10 фотографий.")
        await message.answer("Какое количество фотографий хотите загрузить?")
    except:
        await message.answer("Вы написали символ.\nПопробуйте ещё раз")
            

async def auto_count_photo(message: types.Message, state: FSMContext):
    try:
        if (int(message.text) <= 10) and (int(message.text) >= 1):
            async with state.proxy() as data:
                data['count_photo'] = message.text
                await Auto_Data.next()
                await message.answer("Добавьте фотографии для автомобиля.")
                await message.answer("Добавляйте фото по отдельности!")
        else:
            await message.answer("Вы выбрали больше 10 или меньше 1 фотографии.\nПопробуйте ещё раз")
    except:
        await message.answer("Вы написали символ.\nПопробуйте ещё раз")
    


async def auto_photo(message: types.Message, state: FSMContext):
    global list_photo
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
        list_photo.append(data['photo'])
        if int(data['count_photo']) == len(list_photo):
            await Auto_Data.next()
            await message.answer("Добавьте описание для автомобиля")


async def auto_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await Auto_Data.next()
    await message.answer("Укажите адрес")
    
    
async def auto_address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['address'] = message.text
    await Auto_Data.next()
    await message.answer("Укажите цену автомобия")
    

async def auto_price(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['price'] = int(message.text)
        await Auto_Data.next()
        await message.answer("Ваше Имя")
    except:
        await message.answer("Вы написали символ.\nПопробуйте ещё раз")
        
        
async def auto_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await Auto_Data.next()
    await message.answer("Ваша Фамилия")
        
        
async def auto_last_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['last_name'] = message.text
    await Auto_Data.next()
    await message.answer("Введите номер телефона: ")

async def phone_number(message: types.Message, state: FSMContext):
    global list_photo, id_user
    async with state.proxy() as data:
        data['phone_number'] = message.text
        
        data['day'] = day_week(date.weekday())
        data['mday'] = str(result.tm_mday)
        data['mon_day'] = str(result.tm_mon)
        data['year_day'] = str(result.tm_year)
        id_user = str(message.chat.id)
        fname = str(message.from_user.first_name)
        lname = str(message.from_user.last_name)
        uname = '@' + str(message.from_user.username)
        status = "NO"
        
        media_photo = [types.InputMediaPhoto(list_photo[0], f"Пришла заявка от пользователя: {data['name']} {data['last_name']}\n"
                                                            f"{data['day']}. Дата: {data['mday']}.{data['mon_day']}.{data['year_day']} Время: {result.tm_hour}:{result.tm_min}:{result.tm_sec} \n"
                                                            f"Автомобиль: {data['marka']} {data['model']} Цена: {data['price']:,} руб\n"
                                                            f"Марка: {data['marka']}\n"
                                                            f"Модель: {data['model']}\n"
                                                            f"Год: {data['year']}\n"
                                                            f"Описание: {data['description']}\n"
                                                            f"Адрес: {data['address']}\n"
                                                            f"Телефон: {data['phone_number']}\n"
                                                            f"Цена: {data['price']:,} руб\n")]
        for i in list_photo:
            media_photo.append(types.InputMediaPhoto(i))
        media_photo.pop(1)
        
        await bot.send_media_group(smauto_bot, media_photo)
        sent_message_i = await bot.send_message(smauto_bot, f"Пришла заявка от пользователя: {data['name']} {data['last_name']}\n"
                                        f"{data['day']}. Дата: {data['mday']}.{data['mon_day']}.{data['year_day']} Время: {result.tm_hour}:{result.tm_min}:{result.tm_sec} \n"
                                        f"Автомобиль: {data['marka']} {data['model']} Цена: {data['price']:,} руб\n", reply_markup=check_auto_yes_and_no(id_user))
        
        await bot.send_message(message.chat.id, text="Ваша заявка отправлена на проверку администрации. Дождитесь ответа", reply_markup=kb_start)
        
        sent_message_i = str(sent_message_i.message_id)
        
        sql_add_command_check(data['marka'], data['model'], data['year'], list_photo, data['description'], data['address'], data['price'], data['name'], data['last_name'], data['phone_number'], data['day'], data['mday'], data['mon_day'], data['year_day'], id_user, fname, lname, uname, status, sent_message_i)
        sql_add_users(id_user, data['name'], data['last_name'], data['phone_number'], fname, lname, uname)

        print("Добавление автомобиля на проверку в базу занесено")
    list_photo = []
    await state.finish()


def register_handlers_form(dp: Dispatcher):
    dp.register_message_handler(auto_form_start, commands=['Продолжить'],state=None)
    dp.register_message_handler(auto_marka, state=Auto_Data.marka)
    dp.register_message_handler(auto_model, state=Auto_Data.model)
    for _ in range(3):
        dp.register_message_handler(auto_year, state=Auto_Data.year)
    for _ in range(3):
        dp.register_message_handler(auto_count_photo, state=Auto_Data.count_photo)
    for _ in range(3):
        dp.register_message_handler(auto_photo, content_types=['photo'], state=Auto_Data.photo)
    dp.register_message_handler(auto_description, state=Auto_Data.description)
    dp.register_message_handler(auto_address, state=Auto_Data.address)
    for _ in range(3):
        dp.register_message_handler(auto_price, state=Auto_Data.price)
    dp.register_message_handler(auto_name, state=Auto_Data.name)
    dp.register_message_handler(auto_last_name, state=Auto_Data.last_name)
    dp.register_message_handler(phone_number, state=Auto_Data.phone_number)
    