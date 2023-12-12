from aiogram import Bot, Dispatcher, types
from aiogram.utils.exceptions import TerminatedByOtherGetUpdates, NetworkError
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from keyboard import kb_start, kb_price_range, kb_form, kb_continue_form
from sent_form import register_handlers_form, date, result
from week import day_week
from data.form_data import sql_start_auto, sql_start_users, sql_start_auto_check, sql_start_users_viewing, sql_my_remove_auto
from data.form_data import sql_my_auto, sql_add_users_viewing, sql_check_yes, sql_check_no, sql_add_user_for_check_auto
from data.form_data import sql_select_50_150, sql_select_150_300, sql_select_300_1, sql_select_1
from data.form_data import sql_viewing_50_150, sql_viewing_150_300, sql_viewing_300_1, sql_viewing_1
from data.form_data import sql_owner_50_150, sql_owner_150_300, sql_owner_300_1, sql_owner_1
from dotenv import load_dotenv
import os

START_WELCOME = '''
Добро пожаловать в SMAUTO - бот для продажи и покупки машин!
'''

BUY_AUTO = '''
Выберите ценовой диапазон:
1. 50к. - 150к.
2. 150к. - 300к.
3. 300к. - 1млн.
'''

TO_SELL_AUTO = '''
Чтобы продать автомобиль нужно будет заполнить форму.
После ваша форма пройдет проверку и будет опубликована в SMAuto.
'''

WELCOME_BACK = '''
Главное меню!
'''

load_dotenv()
TOKEN = token = os.environ.get("TOKEN")

bot = Bot(TOKEN)                                  #  
dp = Dispatcher(bot, storage=MemoryStorage())     #  Важные токены для отправки
                                                  #  и запуска бота
admin_id_alex = 1387002896                        #          
smauto_bot = "-1001861129956"                     #


print("Бот активирован")

@dp.message_handler(commands=["start"])           # ------------
async def start_command(message: types.Message):  # 
    await message.answer(text=START_WELCOME,      # Старт бота
                        reply_markup=kb_start)    # 
    await message.delete()                        #--------------

register_handlers_form(dp) #Форма для продажи автомобиля

sql_start_auto()                 #Запуск базы данных
sql_start_users()
sql_start_auto_check()
sql_start_users_viewing()

#Перемещение по страницам --------------------------------------------------------------

@dp.message_handler(text= ["Купить", "Продать", "Мои авто", "Поддержать"])
async def sent_print(message: types.Message):
    if "Купить" == message.text:
        sql_add_users_viewing(str(message.chat.id), str(message.from_user.first_name), str(message.from_user.last_name), ('@' + str(message.from_user.username)), day_week(date.weekday()), str(result.tm_mday), str(result.tm_mon), str(result.tm_year))
        await bot.send_message(message.chat.id,
                               text=BUY_AUTO,
                               reply_markup=kb_price_range)
        await bot.delete_message(message.chat.id, message.message_id)
        #await message.delete()
        
    elif "Продать" == message.text:
        await bot.send_message(message.chat.id,
                               text=TO_SELL_AUTO,
                               reply_markup=kb_form)
        await message.delete()
        
    elif "Мои авто" == message.text:
        if await sql_my_auto(message) == "NO":
            await bot.send_message(message.chat.id, text="Вашего автомобиля нет")
        await message.delete()
        
    elif "Поддержать" == message.text:
        await bot.send_message(message.chat.id, text=f"Поддержать Telegram Bot\n"
                                                    f"Скидка на покупку автомобиля:\n"
                                                    f"1.000 руб - от 1% до 20% на 5 продаж от 1.000 до 20.000 руб")

@dp.message_handler(text= ["Заполнить форму"])
async def sent_print_sell(message: types.Message):
    if "Заполнить форму" == message.text:
        await bot.send_message(message.chat.id, text="Спасибо, что пользуютесь нашим Telegram Ботом", reply_markup=kb_continue_form)
        await message.delete()
        
@dp.message_handler(text= ["Назад"])
async def sent_print_back(message: types.Message):
    global next_auto_50_150, next_auto_150_300, next_auto_300_1, next_auto_1, sum_50_150, sum_150_300, sum_300_1, sum_1
    if "Назад" == message.text:
        await bot.send_message(message.chat.id,
                               text=WELCOME_BACK,
                               reply_markup=kb_start)
        await message.delete()
        
        next_auto_50_150 = -1
        next_auto_150_300 = -1
        next_auto_300_1 = -1
        next_auto_1 = -1
        
        sum_50_150 = 1
        sum_150_300 = 1
        sum_300_1 = 1
        sum_1 = 1

#КУПИТЬ АВТО------------------------------------------

next_auto_50_150 = -1
next_auto_150_300 = -1
next_auto_300_1 = -1
next_auto_1 = -1

@dp.message_handler(text= ["50к - 150к", "150к - 300к", "300к - 1 млн", "1млн+"])
async def sent_price(message: types.Message):
    global next_auto_50_150, next_auto_150_300, next_auto_300_1, next_auto_1
    
    if "50к - 150к" == message.text:
        if await sql_select_50_150(message, -1) != "NO":
            await sql_select_50_150(message, 0)
            next_auto_50_150 = 0
        else:
            await bot.send_message(message.chat.id, text="Пока, ничего нет за 50к - 150к")
            
    elif "150к - 300к" == message.text:
        if await sql_select_150_300(message, -1) != "NO":
            await sql_select_150_300(message, 0)
            next_auto_150_300 = 0
        else:
            await bot.send_message(message.chat.id, text="Пока, ничего нет за 150к - 300к")
            
    elif "300к - 1 млн" == message.text:
        if await sql_select_300_1(message, -1) != "NO":
            await sql_select_300_1(message, 0)
            next_auto_300_1 = 0
        else:
            await bot.send_message(message.chat.id, text="Пока, ничего нет за 300к - 1 млн")
    elif "1млн+" == message.text:
        if await sql_select_1(message, -1) != "NO":
            await sql_select_1(message, 0)
            next_auto_1 = 0
        else:
            await bot.send_message(message.chat.id, text="Пока, ничего нет за 1 млн+")
            
#Следующее авто------------------------------------------------------------------

sum_50_150 = 1
sum_150_300 = 1
sum_300_1 = 1
sum_1 = 1

@dp.message_handler(text= ["Следующее авто"])
async def sent_auto(message: types.Message):
    global next_auto_50_150, next_auto_150_300, next_auto_300_1, next_auto_1, sum_50_150, sum_150_300, sum_300_1, sum_1
    
    if next_auto_50_150 != -1:
        next_auto_50_150 = sum_50_150
        if await sql_select_50_150(message, next_auto_50_150) != "stop":
            sum_50_150 = sum_50_150 + 1
        else:
            next_auto_50_150 = -1
            sum_50_150 = 1
        
    elif next_auto_150_300 != -1:
        next_auto_150_300 = sum_150_300
        if await sql_select_150_300(message, next_auto_150_300) != "stop":
            sum_150_300 = sum_150_300 + 1
        else:
            next_auto_150_300 = -1
            sum_150_300 = 1
        
    elif next_auto_300_1 != -1:
        next_auto_300_1 = sum_300_1
        if await sql_select_300_1(message, next_auto_300_1) != "stop":
            sum_300_1 = sum_300_1 + 1
        else:
            next_auto_300_1 = -1
            sum_300_1 = 1
        
    elif next_auto_1 != -1:
        next_auto_1 = sum_1
        if await sql_select_1(message, next_auto_1) != "stop":
            sum_1 = sum_1 + 1
        else:
            next_auto_1 = -1
            sum_1 = 1

#Посмотреть авто----------------------------------------------------------

@dp.message_handler(text= ["Посмотреть авто"])
async def sent_auto_viewing(message: types.Message):
    global next_auto_50_150, next_auto_150_300, next_auto_300_1, next_auto_1
    if next_auto_50_150 != -1:
        await sql_viewing_50_150(message, next_auto_50_150)
        
    elif next_auto_150_300 != -1:
        await sql_viewing_150_300(message, next_auto_150_300)
        
    elif next_auto_300_1 != -1:
        await sql_viewing_300_1(message, next_auto_300_1)
        
    elif next_auto_1 != -1:
        await sql_viewing_1(message, next_auto_1)

#Связь с владельцем автомобиля--------------------------------------------

@dp.message_handler(text= ["Связаться с владельцем"])
async def sent_auto_contact(message: types.Message):
    global next_auto_50_150, next_auto_150_300, next_auto_300_1, next_auto_1
    if next_auto_50_150 != -1:
        await sql_owner_50_150(message, next_auto_50_150)
        
    elif next_auto_150_300 != -1:
        await sql_owner_150_300(message, next_auto_150_300)
        
    elif next_auto_300_1 != -1:
        await sql_owner_300_1(message, next_auto_300_1)
        
    elif next_auto_1 != -1:
        await sql_owner_1(message, next_auto_1)

#Удаление лишние сообшений--------------------------------------------------

@dp.message_handler()
async def delete_message(message: types.Message):
    await message.delete()

#Изменить или удалить объявление-----------------------------------------------

#@dp.callback_query_handler()
#async def delete_my_auto(callback: types.CallbackQuery):
#    if callback.data == "1":
#        print(123)

#Подтвердить объявление-----------------------------------------------------------

@dp.callback_query_handler()
async def form_yes_no(callback: types.CallbackQuery):
    users = sql_add_user_for_check_auto()
    for id_users in users:
        if callback.data == f"YES_{str(id_users)}":
            await sql_check_yes(id_users)
            await callback.answer("Объявление выложено")
            break
        elif callback.data == f"NO_{str(id_users)}":
            await sql_check_no(id_users)
            await callback.answer("Объявление отклонено")
            break
    id_users_auto_del = str(callback.data)[7:]
    if callback.data == f"delete_{id_users_auto_del}":
        await sql_my_remove_auto(id_users_auto_del)
        id_users_auto_del = 0
        await callback.answer("Объявление снято!")
    else:
        id_users_auto_del = 0
                
    

#ЗАПУСК БОТА ----------------------------------

if __name__ == "__main__":
    try:
        executor.start_polling(dp)
    except TerminatedByOtherGetUpdates as ter:
        print(ter)
    except NetworkError as net:
        print(net)