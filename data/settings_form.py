from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher, Bot
from config import TOKEN_API
from data.form_data import sql_price_settings, sql_description_settings, sql_phone_number_settings, sql_address_settings
from keyboard import kb_remove


bot = Bot(TOKEN_API)


smauto_bot = "-1001861129956"

class Auto_Data_Settings_Price(StatesGroup):
    price = State()
    
class Auto_Data_Settings_Address(StatesGroup):
    address = State()
    
class Auto_Data_Settings_Description(StatesGroup):
    description = State()
    
class Auto_Data_Settings_Phone_Number(StatesGroup):
    phone_number = State()
    
    
async def auto_settings_price(message: types.Message, state: FSMContext):
    global list_id
    try:
        async with state.proxy() as data:
            data['price'] = message.text

            await sql_price_settings(data['price'], list_id[0])
            
            await state.finish()
            
    except:
        await message.answer("Вы написали символ.\nПопробуйте ещё раз")
        

async def auto_settings_address(message: types.Message, state: FSMContext):
    global list_id
    async with state.proxy() as data:
        data['address'] = message.text
        await sql_address_settings(data['address'], list_id[0])
        
        await state.finish()
        

async def auto_settings_description(message: types.Message, state: FSMContext):
    global list_id
    async with state.proxy() as data:
        data['description'] = message.text
        await sql_description_settings(data['description'], list_id[0])
        
        await state.finish()
        

async def auto_settings_phone_number(message: types.Message, state: FSMContext):
    global list_id
    async with state.proxy() as data:
        data['phone_number'] = message.text
        await sql_phone_number_settings(data['phone_number'], list_id[0])
        
        await state.finish()
    
    
async def register_handlers_form_settings_price(dp: Dispatcher, id_users):
    global list_id
    
    list_id = []
    list_id.append(id_users)
    id_users = list_id[0].split("_")

    await Auto_Data_Settings_Price.price.set()
    await bot.send_message(chat_id= id_users[0], text="Введите новую цену: ", reply_markup=kb_remove)
    
    for _ in range(3):
        dp.register_message_handler(auto_settings_price, state= Auto_Data_Settings_Price.price)
        

async def register_handlers_form_settings_address(dp: Dispatcher, id_users):
    global list_id
    
    list_id = []
    list_id.append(id_users)
    id_users = list_id[0].split("_")

    await Auto_Data_Settings_Address.address.set()
    await bot.send_message(chat_id= id_users[0], text="Введите новый адрес: ", reply_markup=kb_remove)
    
    dp.register_message_handler(auto_settings_address, state= Auto_Data_Settings_Address.address)
    
    
async def register_handlers_form_settings_description(dp: Dispatcher, id_users):
    global list_id
    
    list_id = []
    list_id.append(id_users)
    id_users = list_id[0].split("_")

    await Auto_Data_Settings_Description.description.set()
    await bot.send_message(chat_id= id_users[0], text="Введите новое описание: ", reply_markup=kb_remove)
    
    dp.register_message_handler(auto_settings_description, state= Auto_Data_Settings_Description.description)


async def register_handlers_form_settings_phone_number(dp: Dispatcher, id_users):
    global list_id
    
    list_id = []
    list_id.append(id_users)
    id_users = list_id[0].split("_")

    await Auto_Data_Settings_Phone_Number.phone_number.set()
    await bot.send_message(chat_id= id_users[0], text="Введите новый номер телефона: ", reply_markup=kb_remove)
    
    dp.register_message_handler(auto_settings_phone_number, state= Auto_Data_Settings_Phone_Number.phone_number)