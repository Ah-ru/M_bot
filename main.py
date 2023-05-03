from telebot import TeleBot
from telebot.types import *
from contextlib import closing
from config import *
import sqlite3

admin_mode = False
bot = TeleBot(token)



class Keyboard:
    @staticmethod
    def welcome_keyboard():
        keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        button1 = KeyboardButton("/write_message")
        button2 = KeyboardButton("/admin")
        return keyboard.add(button1, button2)
    
    @staticmethod   
    def user_keyboard():
        keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        button1 = KeyboardButton("/send")
        button2 = KeyboardButton("/go_main")
        return keyboard.add(button1, button2)
    
    @staticmethod
    def main_menu():
        keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        button1 = KeyboardButton("/go_main")
        return keyboard.add(button1)
    
    @staticmethod
    def admin_keyboard():
        keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        button1 = KeyboardButton("/read_messages")
        button2 = KeyboardButton("/delete_all_messages")
        button3 = KeyboardButton("/settings")
        button4 = KeyboardButton("/go_main")
        return keyboard.add(button1, button2, button3, button4)

    @staticmethod  
    def confirm():
        keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        button1 = KeyboardButton("/confirm_deletion_all_messages")
        button2 = KeyboardButton("/go_main")
        return keyboard.add(button1, button2)
    
    @staticmethod  
    def confirm_keyboard():
        keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        button1 = KeyboardButton("/Yes")
        button2 = KeyboardButton("/No")
        return keyboard.add(button1,button2)

    @staticmethod
    def new_pass_settings_keyboard():
        keyboard = InlineKeyboardMarkup(row_width=2)
        return keyboard.add(InlineKeyboardButton(text="Set new password",callback_data = "passwd"))
    
    @staticmethod
    def after_passwd_keyboard():
        Keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        button1 = KeyboardButton("/back")
        button2 = KeyboardButton("/go_main")
        return Keyboard.add(button1, button2)


@bot.message_handler(commands=["start", "help", "go_main"])
def welcome(message: Message):
    bot.send_message(message.from_user.id, "Привет! Выбери следующие команды:\nДля того что бы оставить сообщение нажмите на кнопку /write_message",reply_markup=Keyboard.welcome_keyboard())


@bot.message_handler(commands=["write_message"])
def write(message: Message):
    ans = bot.send_message(message.from_user.id, "Хорошо, напишите сообщение\nпосле отправки его боту\nОБЯЗАТЕЛЬНО нажмите кнопку /send\nДля возвращения на главную, нажмите кнопку /go_main",reply_markup=Keyboard.user_keyboard())
    bot.register_next_step_handler(ans, insert_message)

    
def insert_message(message: Message):
    global con, tab
    con = sqlite3.connect(database, check_same_thread=False)
    tab = con.cursor()
    tab.execute("INSERT INTO user_message VALUES (?,?,?)",(message.from_user.id, message.from_user.username,message.text ))    
    
@bot.message_handler(commands=["send"])
def post(message: Message):
    bot.send_message(message.from_user.id, "Спасибо за сообщение)\nнажмите /go_main дял перехода в главное меню", reply_markup=Keyboard.main_menu())
    con.commit()
    con,tab.close()




#admin part
@bot.message_handler(commands=['admin'])
def admin_enter(message: Message):
    if admin_mode:
        bot.send_message(message.from_user.id, "You admin",reply_markup=Keyboard.admin_keyboard())
    else:
        ans = bot.send_message(message.from_user.id, "Enter admin password",reply_markup=Keyboard.main_menu())
        bot.register_next_step_handler(ans, enter_pass)

def enter_pass(message: Message):
    with closing(sqlite3.connect(database)) as con:
        with closing(con.cursor()) as tab:
            passwd = ' '.join(map(str, tab.execute("SELECT real_password FROM bot_params").fetchall().pop()))
    if passwd == message.text:
        bot.send_message(message.from_user.id, "Pass\nYou are in the admin panel\nYou can click on buttons in menu", reply_markup=Keyboard.admin_keyboard())
        global admin_mode
        admin_mode = True
    else:
        bot.send_message(message.from_user.id, "You enter incorrect password",reply_markup=Keyboard.main_menu())  


# @bot.message_handler(commands=["all_commands"])
# def read_messages(call: CallbackQuery):
#     bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
#     bot.send_message(chat_id=call.message.chat.id, text = "All admin commands:",reply_markup = Keyboard.admin_keyboard())





@bot.message_handler(commands=["settings", "back"])
def read_messages(message: Message):
        if admin_mode:
            bot.send_message(message.from_user.id, text = "To go to other admin commands click /all_commands\nOr click /go_main to go to main menu", reply_markup = Keyboard.admin_keyboard()) 
            bot.send_message(message.from_user.id, "Setting commands:",reply_markup = Keyboard.new_pass_settings_keyboard())
        else:
            bot.send_message(message.from_user.id, "sorry, you are not the admin.",reply_markup=Keyboard.main_menu())


@bot.callback_query_handler(func=lambda call: call.data == "passwd")
def passwd_button(call: CallbackQuery): 
    global con, tab
    con = sqlite3.connect(database,check_same_thread=False)
    tab = con.cursor()
    passwd = ' '.join(map(str, tab.execute("SELECT real_password FROM bot_params").fetchall().pop()))
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
    ans = bot.send_message(chat_id=call.message.chat.id, text= f"Real Password =  {passwd}\nEnter new password")
    bot.register_next_step_handler(ans, passwd_new)
    

def passwd_new(message : Message):
    bot.send_message(message.from_user.id, text=f"New password = {message.text}\nConfirm password\nClick Yes or No",reply_markup= Keyboard.confirm_keyboard())
    tab.execute(f"UPDATE bot_params SET real_password = ('{message.text}')")


@bot.message_handler(commands=["Yes"])
def pass_yes(message: Message):
    if admin_mode:
        bot.send_message(message.from_user.id, text = "Password was update\nClick '/back' to go to settings\nClick '/go_main' to go to main menu",reply_markup=Keyboard.after_passwd_keyboard())
        con.commit()
        con,tab.close()
    else:
        bot.send_message(message.from_user.id, "sorry, you are not the admin.",reply_markup=Keyboard.main_menu())
    
@bot.message_handler(commands=["No"])
def pass_no(message: Message):
    if admin_mode:
        con,tab.close()
        bot.send_message(message.from_user.id, text = "Password wasn't update\nClick '/back' to go to settings\nClick '/go_main' to go to main menu",reply_markup=Keyboard.after_passwd_keyboard())
    else:
        bot.send_message(message.from_user.id, "sorry, you are not the admin.",reply_markup=Keyboard.main_menu())


@bot.message_handler(commands=["read_messages"])
def read_messages(message: Message):
    with closing(sqlite3.connect(database)) as con:
        with closing(con.cursor()) as tab:
            if admin_mode: 
                count = 0
                while True:
                    try:
                        bot.send_message(message.from_user.id, ' '.join(map(str, tab.execute("SELECT id, username, message FROM user_message").fetchall().pop(count))))
                        count +=1
                    except:
                        break  
            else:
                bot.send_message(message.from_user.id, "sorry, you are not the admin.",reply_markup=Keyboard.main_menu())


@bot.message_handler(commands=["delete_all_messages"])
def confirm_delete_all(message: Message):
    if admin_mode:
        global con, tab
        con = sqlite3.connect(database, check_same_thread=False)
        tab = con.cursor() 
        tab.execute("DELETE FROM user_message")
        bot.send_message(message.from_user.id, "Danger! All messages will delete!",reply_markup=Keyboard.confirm())
    else:
        bot.send_message(message.from_user.id, "sorry, you are not the admin.",reply_markup=Keyboard.main_menu())


@bot.message_handler(commands=["confirm_deletion_all_messages"])
def delete_all(message: Message):
    if admin_mode: 
        con.commit()
        con, tab.close()
        bot.send_message(message.from_user.id, "all messages was deleted.",reply_markup=Keyboard.admin_keyboard())
    else:
        bot.send_message(message.from_user.id, "sorry, you are not the admin.",reply_markup=Keyboard.main_menu())


bot.polling(non_stop = True) 