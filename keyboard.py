from aiogram import types


kb_start = types.ReplyKeyboardMarkup(resize_keyboard=True)
kb_price = types.KeyboardButton("Купить")
kb_sell = types.KeyboardButton("Продать")
kb_my_auto = types.KeyboardButton("Мои авто")
kb_help = types.KeyboardButton("Поддержать")
kb_start.add(kb_price, kb_sell, kb_my_auto, kb_help)

kb_price_range = types.ReplyKeyboardMarkup(resize_keyboard=True)
kb_50_150 = types.KeyboardButton("0 - 150к")
kb_150_300 = types.KeyboardButton("150к - 300к")
kb_300_1lm = types.KeyboardButton("300к - 1 млн")
kb_1lm_plus = types.KeyboardButton("1млн+")
kb_back = types.KeyboardButton("Назад")
kb_price_range.add(kb_50_150, kb_150_300, kb_300_1lm, kb_1lm_plus, kb_back)

kb_viewing = types.ReplyKeyboardMarkup(resize_keyboard=True)
kb_continue_viewing = types.KeyboardButton("Следующее авто")
kb_auto_viewing = types.KeyboardButton("Посмотреть авто")
kb_viewing.add(kb_continue_viewing, kb_auto_viewing, kb_back)

kb_form = types.ReplyKeyboardMarkup(resize_keyboard=True)
kb_continue = types.KeyboardButton("Заполнить форму")
kb_back = types.KeyboardButton("Назад")
kb_form.add(kb_continue, kb_back)

kb_back_global = types.ReplyKeyboardMarkup(resize_keyboard=True)
kb_back_global.add(kb_back)

kb_contact = types.ReplyKeyboardMarkup(resize_keyboard=True)
kb_contact_auto = types.KeyboardButton("Связаться с владельцем")
kb_contact.add(kb_continue_viewing, kb_contact_auto)

kb_continue_form = types.ReplyKeyboardMarkup(resize_keyboard=True)
kb_con_form = types.KeyboardButton("/Продолжить")
kb_continue_form.add(kb_con_form)

kb_end = types.ReplyKeyboardMarkup(resize_keyboard=True)
kb_end.add(kb_continue_viewing, kb_back)

kb_remove = types.ReplyKeyboardRemove()


def check_auto_yes_and_no(user_id):
    kb_yes_and_no = types.InlineKeyboardMarkup(resize_keyboard=True)
    kb_yes = types.InlineKeyboardButton("Выложить", callback_data=f"YES_{user_id}")
    kb_no = types.InlineKeyboardButton("Отклонить", callback_data=f"NO_{user_id}")
    kb_yes_and_no.add(kb_yes, kb_no)
    
    return kb_yes_and_no


def change_del(auto):
    kb_change_del = types.InlineKeyboardMarkup(resize_keyboard=True)
    kb_change = types.InlineKeyboardButton("Изменить объявление", callback_data=f"change")
    kb_del = types.InlineKeyboardButton("Снять объявление",callback_data=f"delete_{auto[-1]}")
    kb_change_del.add(kb_change, kb_del)
    
    return kb_change_del
