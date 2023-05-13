from telebot import TeleBot
from telebot.types import *
from contextlib import closing
from config import *
import sqlite3

bot = TeleBot(token)

global mes, username, user_id
global new_passwd
mes = username = user_id = None
new_passwd = '0000'

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
        return keyboard.add(button1, button2)

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

    @staticmethod
    def delete():
        delete  =  ReplyKeyboardRemove()
        return delete 
    
    @staticmethod
    def all_commands():
        Keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        button1 = KeyboardButton("/all_commands")
        button2 = KeyboardButton("/go_main")
        return Keyboard.add(button1, button2)


def exam_admin(admin_id):
    with closing(sqlite3.connect(database)) as con:
        with closing(con.cursor()) as tab:
            global admin_passwd 
            global passwd 
            passwd = ' '.join(map(str, tab.execute("SELECT real_password FROM bot_params").fetchall().pop()))
            try:     
                admin_passwd = ' '.join(map(str, tab.execute("SELECT password FROM admin WHERE id = (?) ", (admin_id,)).fetchall().pop()))
            except:
                admin_passwd = ' '


@bot.message_handler(commands=["start", "help", "go_main"])
def welcome(message: Message):
    bot.send_message(message.from_user.id, "Привет! Выбери следующие команды:\nДля того что бы оставить сообщение нажмите на кнопку /write_message", reply_markup = Keyboard.welcome_keyboard())


@bot.message_handler(commands=["write_message"])
def write(message: Message):
    ans = bot.send_message(message.from_user.id, "Хорошо, напишите сообщение\nПосле отправки его боту\nОБЯЗАТЕЛЬНО нажмите кнопку /send\nДля возвращения на главную, нажмите кнопку /go_main", reply_markup = Keyboard.user_keyboard())
    bot.register_next_step_handler(ans, insert_message)

    
def insert_message(message: Message):
    global mes, username, user_id
    mes = message.text
    username = message.from_user.username
    user_id  = message.from_user.id


@bot.message_handler(commands=["send"])
def post(message: Message):
    if mes.startswith('/') or mes == None:
        bot.send_message(message.from_user.id, "Спам и ложные сообщения не записываются в базу.", reply_markup = Keyboard.main_menu())
    else:
        bot.send_message(message.from_user.id, "Спасибо за сообщение)\nНажмите /go_main для перехода в главное меню", reply_markup = Keyboard.main_menu())
        with closing(sqlite3.connect(database)) as con:
            with closing(con.cursor()) as tab:
                tab.execute("INSERT INTO user_message VALUES (?,?,?)", (user_id, username, mes))    
                con.commit()




#admin_part
@bot.message_handler(commands=['admin'])
def admin_enter(message: Message):
    admin_id = message.from_user.id
    with closing(sqlite3.connect(database)) as con:
        with closing(con.cursor()) as tab:
            try:
                admin_passwd = ' '.join(map(str, tab.execute("SELECT password FROM admin WHERE id = (?) ", (admin_id,)).fetchall().pop()))#Pass for 
                passwd = ' '.join(map(str, tab.execute("SELECT real_password FROM bot_params").fetchall().pop()))
                if admin_passwd == passwd:
                    bot.send_message(message.from_user.id, "Pass\nYou are in the admin panel\nYou can click on buttons in menu", reply_markup = Keyboard.admin_keyboard())
                else:
                    ans = bot.send_message(message.from_user.id, "Enter admin password", reply_markup = Keyboard.main_menu())
                    bot.register_next_step_handler(ans, enter_pass)
            except:
                ans = bot.send_message(message.from_user.id, "Enter admin password", reply_markup = Keyboard.main_menu())
                bot.register_next_step_handler(ans, enter_pass)
            
            
def enter_pass(message: Message):
    admin_id = message.from_user.id
    with closing(sqlite3.connect(database)) as con:
        with closing(con.cursor()) as tab:
            passwd = ' '.join(map(str, tab.execute("SELECT real_password FROM bot_params").fetchall().pop()))
            if passwd == message.text:
                bot.send_message(message.from_user.id, "Pass\nYou are in the admin panel\nYou can click on buttons in menu", reply_markup = Keyboard.admin_keyboard())
                tab.execute("DELETE FROM admin WHERE id = (?)", (admin_id,))
                tab.execute("INSERT INTO admin VALUES (?,?)", (admin_id, passwd))
                con.commit()
            else:
                bot.send_message(message.from_user.id, "You enter incorrect password", reply_markup = Keyboard.main_menu())  


@bot.message_handler(commands=["all_commands"])
def read_messages(message: Message):
    exam_admin(message.from_user.id)
    if passwd == admin_passwd:
        bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)
        bot.delete_message(chat_id=message.chat.id, message_id=message.id - 2)
        bot.send_message(message.from_user.id, "All admin commands:", reply_markup = Keyboard.admin_keyboard())
    else:
        bot.send_message(message.from_user.id, "sorry, you are not the admin.", reply_markup = Keyboard.main_menu())


@bot.message_handler(commands=["settings", "back"])
def read_messages(message: Message):
    exam_admin(message.from_user.id)
    if passwd == admin_passwd:
        bot.send_message(message.from_user.id, text = "To go to other admin commands click /all_commands\nOr click /go_main to go to main menu", reply_markup = Keyboard.all_commands()) 
        bot.send_message(message.from_user.id, "Setting commands:", reply_markup = Keyboard.new_pass_settings_keyboard())
    else:
        bot.send_message(message.from_user.id, "sorry, you are not the admin.", reply_markup = Keyboard.main_menu())


@bot.callback_query_handler(func=lambda call: call.data == "passwd")
def passwd_button(call: CallbackQuery): 
    with closing(sqlite3.connect(database)) as con:
        with closing(con.cursor()) as tab:
            passwd = ' '.join(map(str, tab.execute("SELECT real_password FROM bot_params").fetchall().pop()))
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
    ans = bot.send_message(chat_id=call.message.chat.id, text= f"Real Password =  {passwd}\nEnter new password", reply_markup = Keyboard.delete())
    bot.register_next_step_handler(ans, passwd_new)
    

def passwd_new(message : Message):
    bot.send_message(message.from_user.id, text=f"New password = {message.text}\nConfirm password\nClick Yes or No", reply_markup = Keyboard.confirm_keyboard())
    global new_passwd
    new_passwd = message.text


@bot.message_handler(commands=["Yes"])
def pass_yes(message: Message):
    exam_admin(message.from_user.id)
    if passwd == admin_passwd:
        bot.send_message(message.from_user.id, text = f"Password was update, password = {new_passwd}\nClick '/back' to go to settings\nClick '/go_main' to go to main menu", reply_markup = Keyboard.after_passwd_keyboard())
        with closing(sqlite3.connect(database)) as con:
            with closing(con.cursor()) as tab:
                tab.execute(f"UPDATE bot_params SET real_password = ('{new_passwd}')")
                con.commit()
    else:
        bot.send_message(message.from_user.id, "sorry, you are not the admin.", reply_markup = Keyboard.main_menu())
    
@bot.message_handler(commands=["No"])
def pass_no(message: Message):
    exam_admin(message.from_user.id)
    if passwd == admin_passwd:
        bot.send_message(message.from_user.id, text = "Password wasn't update\nClick '/back' to go to settings\nClick '/go_main' to go to main menu", reply_markup = Keyboard.after_passwd_keyboard())
    else:
        bot.send_message(message.from_user.id, "sorry, you are not the admin.", reply_markup = Keyboard.main_menu())


@bot.message_handler(commands=["read_messages"])
def read_messages(message: Message):
    exam_admin(message.from_user.id)
    if passwd == admin_passwd:
        with closing(sqlite3.connect(database)) as con:
            with closing(con.cursor()) as tab:
                count = 0
                while True:
                    try:
                        bot.send_message(message.from_user.id, ' '.join(map(str, tab.execute("SELECT id, username, message FROM user_message").fetchall().pop(count))))
                        count +=1
                    except:
                        if count == 0:
                            bot.send_message(message.from_user.id, "No messages.")
                        break                        
    else:
        bot.send_message(message.from_user.id, "sorry, you are not the admin.", reply_markup = Keyboard.main_menu())


@bot.message_handler(commands=["delete_all_messages"])
def delete_all(message: Message):
    exam_admin(message.from_user.id)
    if passwd == admin_passwd:
        bot.send_message(message.from_user.id, "Danger! All messages will delete!", reply_markup = Keyboard.confirm())
    else:
        bot.send_message(message.from_user.id, "sorry, you are not the admin.", reply_markup = Keyboard.main_menu())


@bot.message_handler(commands=["confirm_deletion_all_messages"])
def confirm_delete_all(message: Message):
    exam_admin(message.from_user.id)
    if passwd == admin_passwd: 
        with closing(sqlite3.connect(database)) as con:
            with closing(con.cursor()) as tab:
                tab.execute("DELETE FROM user_message")
                con.commit()
        bot.send_message(message.from_user.id, "all messages was deleted.", reply_markup = Keyboard.admin_keyboard())
    else:
        bot.send_message(message.from_user.id, "sorry, you are not the admin.", reply_markup = Keyboard.main_menu())

bot.polling(non_stop = True) 