import sqlite3 as sq
import json
from aiogram import types, Dispatcher, Bot
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, types
from keyboard import kb_viewing, kb_price_range, kb_contact, kb_end, change_del, kb_back_global
import time
import os.path
import os
from config import TOKEN
#from dotenv import load_dotenv


#load_dotenv()
#TOKEN = token = os.environ.get("TOKEN")

bot = Bot(token= TOKEN)


#Подключение базы данных----------------------------------------------

def sql_start_auto():
    global base, cur
    base = sq.connect("data/form.db")
    cur = base.cursor()
    
    if base:
        print("К базе данных автомобилей произошло подключение")
        
    base.execute('''CREATE TABLE IF NOT EXISTS form_auto(marka TEXT,
                                                        model TEXT,
                                                        year TEXT,
                                                        photo TEXT,
                                                        description TEXT,
                                                        address TEXT,
                                                        price INTEGER,
                                                        name TEXT,
                                                        last_name TEXT,
                                                        phone_number TEXT,
                                                        day TEXT,
                                                        mday TEXT,
                                                        mon_day TEXT,
                                                        year_day TEXT,
                                                        id_user TEXT,
                                                        fname TEXT,
                                                        lname TEXT,
                                                        uname TEXT,
                                                        status TEXT)''')
    base.commit()
 

def sql_start_auto_check():
    global base_ac, cur_ac
    base_ac = sq.connect("data/check_auto.db")
    cur_ac = base.cursor()
    
    if base_ac:
        print("К базе данных для проверки автомобилей произошло подключение")
        
    base_ac.execute('''CREATE TABLE IF NOT EXISTS form_check_auto(marka TEXT,
                                                                model TEXT,
                                                                year TEXT,
                                                                photo TEXT,
                                                                description TEXT,
                                                                address TEXT,
                                                                price INTEGER,
                                                                name TEXT,
                                                                last_name TEXT,
                                                                phone_number TEXT,
                                                                day TEXT,
                                                                mday TEXT,
                                                                mon_day TEXT,
                                                                year_day TEXT,
                                                                id_user TEXT,
                                                                fname TEXT,
                                                                lname TEXT,
                                                                uname TEXT,
                                                                status TEXT)''')
    base_ac.commit()


def sql_start_users():
    global base_u, cur_u
    base_u = sq.connect("data/users.db")
    cur_u = base.cursor()
    
    if base_u:
        print("К базе данных пользователей произошло подключение")
        
    base_u.execute('''CREATE TABLE IF NOT EXISTS users_data(id_user TEXT,
                                                        name TEXT,
                                                        last_name TEXT,
                                                        phone_number TEXT,
                                                        fname TEXT,
                                                        lname TEXT,
                                                        uname TEXT)''')
    base_u.commit()
    

def sql_start_users_viewing():
    global base_uv, cur_uv
    base_uv = sq.connect("data/users_viewing.db")
    cur_uv = base.cursor()
    
    if base_uv:
        print("К базе данных просмотр пользователей произошло подключение")
        
    base_uv.execute('''CREATE TABLE IF NOT EXISTS users_data_viewing(id_user TEXT,
                                                                    fname TEXT,
                                                                    lname TEXT,
                                                                    uname TEXT,
                                                                    day TEXT,
                                                                    mday TEXT,
                                                                    mon_day TEXT,
                                                                    year_day TEXT)''')
    base_uv.commit()

#Добавление машины в базу данных-----------------------------------------------

def sql_add_command(marka, model, year, photo, description, address, price, name, last_name, phone_number, day, mday, mon_day, year_day, id_user, fname, lname, uname, status):
    photo = json.dumps(photo)
    cur.execute(f"INSERT INTO form_auto VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (marka, model, year, photo, description, address, price, name, last_name, phone_number, day, mday, mon_day, year_day, id_user, fname, lname, uname, status))
    base.commit()
    

def sql_add_command_check(marka, model, year, photo, description, address, price, name, last_name, phone_number, day, mday, mon_day, year_day, id_user, fname, lname, uname, status):
    photo = json.dumps(photo)
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "check_auto.db")
    with sq.connect(db_path) as db:
        cur_ac = db.cursor()
        db.execute('''CREATE TABLE IF NOT EXISTS form_check_auto(marka TEXT,
                                                                model TEXT,
                                                                year TEXT,
                                                                photo TEXT,
                                                                description TEXT,
                                                                address TEXT,
                                                                price INTEGER,
                                                                name TEXT,
                                                                last_name TEXT,
                                                                phone_number TEXT,
                                                                day TEXT,
                                                                mday TEXT,
                                                                mon_day TEXT,
                                                                year_day TEXT,
                                                                id_user TEXT,
                                                                fname TEXT,
                                                                lname TEXT,
                                                                uname TEXT,
                                                                status TEXT)''')
        db.commit()
    
        cur_ac.execute(f"INSERT INTO form_check_auto VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (marka, model, year, photo, description, address, price, name, last_name, phone_number, day, mday, mon_day, year_day, id_user, fname, lname, uname, status))
        db.commit()
        
        
def sql_add_users(id_user, name, last_name, phone_number, fname, lname, uname):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "users.db")
    with sq.connect(db_path) as db_u:
        cur_u = db_u.cursor()
        db_u.execute('''CREATE TABLE IF NOT EXISTS users_data(id_user TEXT,
                                                            name TEXT,
                                                            last_name TEXT,
                                                            phone_number TEXT,
                                                            fname TEXT,
                                                            lname TEXT,
                                                            uname TEXT)''')
        db_u.commit()
        
        cur_u.execute("INSERT INTO users_data VALUES (?, ?, ?, ?, ?, ?, ?)", (id_user, name, last_name, phone_number, fname, lname, uname))  
        db_u.commit()


def sql_add_users_viewing(id_user, fname, lname, uname, day, mday, mon_day, year_day):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "users_viewing.db")
    with sq.connect(db_path) as db_uv:
        cur_uv = db_uv.cursor()
        db_uv.execute('''CREATE TABLE IF NOT EXISTS users_data_viewing(id_user TEXT,
                                                                        fname TEXT,
                                                                        lname TEXT,
                                                                        uname TEXT
                                                                        day TEXT,
                                                                        mday TEXT,
                                                                        mon_day TEXT,
                                                                        year_day TEXT)''')
        db_uv.commit()
        
        for id_u in db_uv.execute("SELECT id_user, mday, mon_day, year_day FROM users_data_viewing").fetchall():
            if id_u[0] == id_user and id_u[1] == mday and id_u[2] == mon_day and id_u[3] == year_day:
                return "YES"
        
        cur_uv.execute("INSERT INTO users_data_viewing VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (id_user, fname, lname, uname, day, mday, mon_day, year_day))
        db_uv.commit()
        
        
async def sql_check_yes(id_user):
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "check_auto.db")
    with sq.connect(db_path) as db:
        cur_ac = db.cursor()
        db.execute('''CREATE TABLE IF NOT EXISTS form_check_auto(marka TEXT,
                                                                model TEXT,
                                                                year TEXT,
                                                                photo TEXT,
                                                                description TEXT,
                                                                address TEXT,
                                                                price INTEGER,
                                                                name TEXT,
                                                                last_name TEXT,
                                                                phone_number TEXT,
                                                                day TEXT,
                                                                mday TEXT,
                                                                mon_day TEXT,
                                                                year_day TEXT,
                                                                id_user TEXT,
                                                                fname TEXT,
                                                                lname TEXT,
                                                                uname TEXT,
                                                                status TEXT)''')
        db.commit()
    
        for id in db.execute(f"SELECT id_user, status FROM form_check_auto").fetchall():
            if id_user == id[0]:
                db.commit()
                
                info = db.execute(f"SELECT marka, model, year, photo, description, address, price, name, last_name, phone_number, day, mday, mon_day, year_day, id_user, fname, lname, uname, status FROM form_check_auto WHERE {id_user}").fetchall()
                photo = json.loads(info[0][3])
                sql_add_command(info[0][0], info[0][1], info[0][2], photo, info[0][4], info[0][5], info[0][6], info[0][7], info[0][8], info[0][9], info[0][10], info[0][11], info[0][12], info[0][13], info[0][14], info[0][15], info[0][16], info[0][17], "YES")
                db.commit()
                
                db.execute(f"DELETE FROM form_check_auto WHERE id_user = {id_user}")
                db.commit()
                
                await bot.send_message(id_user, text="Ваше объявление опубликовано!")
        

async def sql_check_no(id_user):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "check_auto.db")
    with sq.connect(db_path) as db:
        cur_ac = db.cursor()
        db.execute('''CREATE TABLE IF NOT EXISTS form_check_auto(marka TEXT,
                                                                model TEXT,
                                                                year TEXT,
                                                                photo TEXT,
                                                                description TEXT,
                                                                address TEXT,
                                                                price INTEGER,
                                                                name TEXT,
                                                                last_name TEXT,
                                                                phone_number TEXT,
                                                                day TEXT,
                                                                mday TEXT,
                                                                mon_day TEXT,
                                                                year_day TEXT,
                                                                id_user TEXT,
                                                                fname TEXT,
                                                                lname TEXT,
                                                                uname TEXT,
                                                                status TEXT)''')
        db.commit()
        
        for id in db.execute(f"SELECT id_user, status FROM form_check_auto").fetchall():
            if id_user == id[0]:
                db.commit()
                
                db.execute(f"DELETE FROM form_check_auto WHERE id_user = {id_user}")
                db.commit()
                
                await bot.send_message(id_user, text="Ваше объявление отклонено! Возможно у вас ошибка в объявление. Попробуйте снова!")

def sql_add_user_for_check_auto():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "check_auto.db")
    with sq.connect(db_path) as db_f:
        cur_f = db_f.cursor()
        db_f.execute('''CREATE TABLE IF NOT EXISTS form_check_auto(id_user TEXT)''')
        db_f.commit()
        users = []
        for id_user in db_f.execute("SELECT id_user FROM form_check_auto").fetchall():
            users.append(id_user[0])

        return users
    
async def sql_my_remove_auto(id_user):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "form.db")
    with sq.connect(db_path) as db_r:
        cur_r = db_r.cursor()
        db_r.execute('''CREATE TABLE IF NOT EXISTS form_auto(marka TEXT,
                                                        model TEXT,
                                                        year TEXT,
                                                        photo TEXT,
                                                        description TEXT,
                                                        address TEXT,
                                                        price INTEGER,
                                                        name TEXT,
                                                        last_name TEXT,
                                                        phone_number TEXT,
                                                        day TEXT,
                                                        mday TEXT,
                                                        mon_day TEXT,
                                                        year_day TEXT,
                                                        id_user TEXT,
                                                        fname TEXT,
                                                        lname TEXT,
                                                        uname TEXT,
                                                        status TEXT)''')
        db_r.commit()
        
        for id in db_r.execute(f"SELECT id_user, status FROM form_auto").fetchall():
            if id_user == id[0]:
                db_r.commit()
                
                db_r.execute(f"DELETE FROM form_auto WHERE id_user = {id_user}")
                db_r.commit()
                
                await bot.send_message(id_user, text="Ваше объявление снято!")
        
#Следующее авто----------------------------------------------------------------    
    
async def sql_select_50_150(message: types.Message, next_auto):
    count_50 = len(cur.execute(f"SELECT marka, model, year, photo, price FROM form_auto WHERE price BETWEEN 50000 AND 150000").fetchall())
    
    if count_50 != 0 and next_auto == -1:
        return "YES"
    
    if count_50 != 0:
        info = cur.execute(f"SELECT marka, model, year, photo, price FROM form_auto WHERE price BETWEEN 50000 AND 150000").fetchall()
        try:
            info = info[next_auto]
            photo = json.loads(info[3])
            await bot.send_photo(message.chat.id, photo[0], f"Автомобиль: {info[0]} {info[1]} {info[2]}\n"
                                                                f"Цена: {info[4]:,}", reply_markup=kb_viewing)
        except IndexError:
                await bot.send_message(message.chat.id, text="Машины закончились!", reply_markup=kb_price_range)
                return "stop"
    else:
        return "NO"
    

async def sql_select_150_300(message: types.Message, next_auto):
    count_150 = len(cur.execute(f"SELECT marka, model, year, photo, price FROM form_auto WHERE price BETWEEN 150000 AND 300000").fetchall())
    
    if count_150 != 0 and next_auto == -1:
        return "YES"
    
    if count_150 != 0:
        info = cur.execute(f"SELECT marka, model, year, photo, price FROM form_auto WHERE price BETWEEN 150000 AND 300000").fetchall()
        try:
            info = info[next_auto]
            photo = json.loads(info[3])
            await bot.send_photo(message.chat.id, photo[0], f"Автомобиль: {info[0]} {info[1]} {info[2]}\n"
                                                                f"Цена: {info[4]:,}", reply_markup=kb_viewing)
        except IndexError:
                await bot.send_message(message.chat.id, text="Машины закончились!", reply_markup=kb_price_range)
                return "stop"
    else:
        return "NO"
        
        
async def sql_select_300_1(message: types.Message, next_auto):
    count_300 = len(cur.execute(f"SELECT marka, model, year, photo, price FROM form_auto WHERE price BETWEEN 300000 AND 1000000").fetchall())
    
    if count_300 != 0 and next_auto == -1:
        return "YES"
    
    if count_300 != 0:
        info = cur.execute(f"SELECT marka, model, year, photo, price FROM form_auto WHERE price BETWEEN 300000 AND 1000000").fetchall()
        try:
            info = info[next_auto]
            photo = json.loads(info[3])
            await bot.send_photo(message.chat.id, photo[0], f"Автомобиль: {info[0]} {info[1]} {info[2]}\n"
                                                                f"Цена: {info[4]:,}", reply_markup=kb_viewing)
        except IndexError:
                await bot.send_message(message.chat.id, text="Машины закончились!", reply_markup=kb_price_range)
                return "stop"
    else:
        return "NO"
        
        
async def sql_select_1(message: types.Message, next_auto):
    count_1 = len(cur.execute(f"SELECT marka, model, year, photo, price FROM form_auto WHERE price > 1000000").fetchall())
    
    if count_1 != 0 and next_auto == -1:
        return "YES"
    
    if count_1 != 0:
        info = cur.execute(f"SELECT marka, model, year, photo, price FROM form_auto WHERE price > 1000000").fetchall()
        try:
            info = info[next_auto]
            photo = json.loads(info[3])
            await bot.send_photo(message.chat.id, photo[0], f"Автомобиль: {info[0]} {info[1]} {info[2]}\n"
                                                                f"Цена: {info[4]:,}", reply_markup=kb_viewing)
        except IndexError:
                await bot.send_message(message.chat.id, text="Машины закончились!", reply_markup=kb_price_range)
                return "stop"
    else:
        return "NO"

#Мои авто на продажу-------------------------------------------------
    
async def sql_my_auto(message: types.Message):
    global my_id_users
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "form.db")
    with sq.connect(db_path) as db:
        cur = db.cursor()
        db.execute('''CREATE TABLE IF NOT EXISTS form_auto(marka TEXT,
                                                        model TEXT,
                                                        year TEXT,
                                                        photo TEXT,
                                                        description TEXT,
                                                        address TEXT,
                                                        price INTEGER,
                                                        name TEXT,
                                                        last_name TEXT,
                                                        phone_number TEXT,
                                                        day TEXT,
                                                        mday TEXT,
                                                        mon_day TEXT,
                                                        year_day TEXT,
                                                        id_user TEXT,
                                                        fname TEXT,
                                                        lname TEXT,
                                                        uname TEXT,
                                                        status TEXT)''')
        db.commit()
        
        for id in cur.execute(f"SELECT id_user FROM form_auto").fetchall():
            if str(message.chat.id) == str(id[0]):
                my_id_users = id[0]
                break
        else:
            my_id_users = 0
                
        db.commit()

        if str(message.chat.id) == str(my_id_users):
            await bot.send_message(message.chat.id , text="Ваши автомобили!", reply_markup=kb_back_global)
            for my_auto in cur.execute(f"SELECT marka, model, year, photo, description, address, price, day, mday, mon_day, year_day, id_user FROM form_auto WHERE id_user == '{message.chat.id}'").fetchall():
                photo = json.loads(my_auto[3])
                media_photo = [types.InputMediaPhoto(photo[0],  f"{my_auto[7]}. Дата: {my_auto[8]}.{my_auto[9]}.{my_auto[10]}\n")]

                for i in photo:
                    media_photo.append(types.InputMediaPhoto(i))
                media_photo.pop(1)
                await bot.send_media_group(message.chat.id, media_photo)
                await bot.send_message(message.chat.id, f"Автомобиль: {my_auto[0]} {my_auto[1]} {my_auto[2]} Цена: {my_auto[6]:,} руб\n"
                                                        f"Марка: {my_auto[0]}\n"
                                                        f"Модель: {my_auto[1]}\n"
                                                        f"Год: {my_auto[2]}\n"
                                                        f"Описание: {my_auto[4]}\n"
                                                        f"Адрес: {my_auto[5]}\n"
                                                        f"Цена: {my_auto[6]:,} руб\n", reply_markup=change_del(my_auto))
                time.sleep(1)
                db.commit()
        else:
            return "NO"
    
#Просмотр авто-----------------------------------------------

async def sql_viewing_50_150(message: types.Message, viewing_auto):
    info = cur.execute(f"SELECT marka, model, year, photo, description, address, price, day, mday, mon_day, year_day FROM form_auto WHERE price BETWEEN 50000 AND 150000").fetchall()
    info = info[viewing_auto]
    photo = json.loads(info[3])
    media_photo = [types.InputMediaPhoto(photo[0],  f"{info[7]}. Дата: {info[8]}.{info[9]}.{info[10]}\n"
                                                            f"Автомобиль: {info[0]} {info[1]} {info[2]} Цена: {info[6]:,} руб\n"
                                                            f"Марка: {info[0]}\n"
                                                            f"Модель: {info[1]}\n"
                                                            f"Год: {info[2]}\n"
                                                            f"Описание: {info[4]}\n"
                                                            f"Адрес: {info[5]}\n"
                                                            f"Цена: {info[6]:,} руб\n")]
    for i in photo:
        media_photo.append(types.InputMediaPhoto(i))
    media_photo.pop(1)
    await bot.send_media_group(message.chat.id, media_photo)
    await bot.send_message(message.chat.id, text="Можете связаться с владельцем авто!", reply_markup=kb_contact)


async def sql_viewing_150_300(message: types.Message, viewing_auto):
    info = cur.execute(f"SELECT marka, model, year, photo, description, address, price, day, mday, mon_day, year_day FROM form_auto WHERE price BETWEEN 150000 AND 300000").fetchall()
    info = info[viewing_auto]
    photo = json.loads(info[3])
    media_photo = [types.InputMediaPhoto(photo[0],  f"{info[7]}. Дата: {info[8]}.{info[9]}.{info[10]}\n"
                                                            f"Автомобиль: {info[0]} {info[1]} {info[2]} Цена: {info[6]:,} руб\n"
                                                            f"Марка: {info[0]}\n"
                                                            f"Модель: {info[1]}\n"
                                                            f"Год: {info[2]}\n"
                                                            f"Описание: {info[4]}\n"
                                                            f"Адрес: {info[5]}\n"
                                                            f"Цена: {info[6]:,} руб\n")]
    for i in photo:
        media_photo.append(types.InputMediaPhoto(i))
    media_photo.pop(1)
    await bot.send_media_group(message.chat.id, media_photo)
    await bot.send_message(message.chat.id, text="Можете связаться с владельцем авто!", reply_markup=kb_contact)


async def sql_viewing_300_1(message: types.Message, viewing_auto):
    info = cur.execute(f"SELECT marka, model, year, photo, description, address, price, day, mday, mon_day, year_day FROM form_auto WHERE price BETWEEN 300000 AND 1000000").fetchall()
    info = info[viewing_auto]
    photo = json.loads(info[3])
    media_photo = [types.InputMediaPhoto(photo[0],  f"{info[7]}. Дата: {info[8]}.{info[9]}.{info[10]}\n"
                                                            f"Автомобиль: {info[0]} {info[1]} {info[2]} Цена: {info[6]:,} руб\n"
                                                            f"Марка: {info[0]}\n"
                                                            f"Модель: {info[1]}\n"
                                                            f"Год: {info[2]}\n"
                                                            f"Описание: {info[4]}\n"
                                                            f"Адрес: {info[5]}\n"
                                                            f"Цена: {info[6]:,} руб\n")]
    for i in photo:
        media_photo.append(types.InputMediaPhoto(i))
    media_photo.pop(1)
    await bot.send_media_group(message.chat.id, media_photo)
    await bot.send_message(message.chat.id, text="Можете связаться с владельцем авто!", reply_markup=kb_contact)


async def sql_viewing_1(message: types.Message, viewing_auto):
    info = cur.execute(f"SELECT marka, model, year, photo, description, address, price, day, mday, mon_day, year_day FROM form_auto WHERE price > 1000000").fetchall()
    info = info[viewing_auto]
    photo = json.loads(info[3])
    media_photo = [types.InputMediaPhoto(photo[0],  f"{info[7]}. Дата: {info[8]}.{info[9]}.{info[10]}\n"
                                                            f"Автомобиль: {info[0]} {info[1]} {info[2]} Цена: {info[6]:,} руб\n"
                                                            f"Марка: {info[0]}\n"
                                                            f"Модель: {info[1]}\n"
                                                            f"Год: {info[2]}\n"
                                                            f"Описание: {info[4]}\n"
                                                            f"Адрес: {info[5]}\n"
                                                            f"Цена: {info[6]:,} руб\n")]
    for i in photo:
        media_photo.append(types.InputMediaPhoto(i))
    media_photo.pop(1)
    await bot.send_media_group(message.chat.id, media_photo)
    await bot.send_message(message.chat.id, text="Можете связаться с владельцем авто!", reply_markup=kb_contact)
    
#Связь с владельцем авто через просмотр его данных через базу----------------

async def sql_owner_50_150(message: types.Message, viewing_auto):
    info = cur.execute(f"SELECT name, last_name, phone_number, fname, lname, uname, address FROM form_auto WHERE price BETWEEN 50000 AND 150000").fetchall()
    info = info[viewing_auto]
    data_owner = f"Имя: {info[0]}\nФамилия: {info[1]}\nНомер телефона: {info[2]}\nТелеграм: {info[3]} {info[4]} или {info[5]}\nАдрес: {info[6]}"
    
    await bot.send_message(message.chat.id, text=data_owner, reply_markup=kb_end)
    

async def sql_owner_150_300(message: types.Message, viewing_auto):
    info = cur.execute(f"SELECT name, last_name, phone_number, fname, lname, uname, address FROM form_auto WHERE price BETWEEN 150000 AND 300000").fetchall()
    info = info[viewing_auto]
    data_owner = f"Имя: {info[0]}\nФамилия: {info[1]}\nНомер телефона: {info[2]}\nТелеграм: {info[3]} {info[4]} или {info[5]}\nАдрес: {info[6]}"
    
    await bot.send_message(message.chat.id, text=data_owner, reply_markup=kb_end)


async def sql_owner_300_1(message: types.Message, viewing_auto):
    info = cur.execute(f"SELECT name, last_name, phone_number, fname, lname, uname, address FROM form_auto WHERE price BETWEEN 300000 AND 1000000").fetchall()
    info = info[viewing_auto]
    data_owner = f"Имя: {info[0]}\nФамилия: {info[1]}\nНомер телефона: {info[2]}\nТелеграм: {info[3]} {info[4]} или {info[5]}\nАдрес: {info[6]}"
    
    await bot.send_message(message.chat.id, text=data_owner, reply_markup=kb_end)
    
    
async def sql_owner_1(message: types.Message, viewing_auto):
    info = cur.execute(f"SELECT name, last_name, phone_number, fname, lname, uname, address FROM form_auto WHERE price > 1000000").fetchall()
    info = info[viewing_auto]
    data_owner = f"Имя: {info[0]}\nФамилия: {info[1]}\nНомер телефона: {info[2]}\nТелеграм: {info[3]} {info[4]} или {info[5]}\nАдрес: {info[6]}"
    
    await bot.send_message(message.chat.id, text=data_owner, reply_markup=kb_end)
    
#Удалить объявление----------------------------------------------

async def sql_my_delete(message: types.Message, viewing_auto):
    pass
