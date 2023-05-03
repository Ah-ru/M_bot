from telebot import TeleBot
from telebot.types import *
import sqlite3


class Admin_params:
    default_pass = 1111
    about = None
    token = "6032634459:AAHeCf7XQKi-8OJC4eEZfZSVCdb4RFVZ5lw"
    database = "telegram_database.db"

bot = TeleBot(Admin_params.token)

con = sqlite3.connect(Admin_params.database,check_same_thread=False)
tab = con.cursor()

class Keyboard:
    def welcome_keyboard():
        keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        button1 = KeyboardButton("/write_message")
        button2 = KeyboardButton("/admin")
        keyboard.add(button1, button2)
        return keyboard 
    def user_keyboard():
        keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        button1 = KeyboardButton("/send")
        button2 = KeyboardButton("/go_main")
        keyboard.add(button1, button2)
        return keyboard
    def main_menu():
        keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        button1 = KeyboardButton("/go_main")
        keyboard.add(button1)
        return keyboard
    def admin_keyboard():
        keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        button1 = KeyboardButton("/read_messages")
        button2 = KeyboardButton("/delete_all_messages")
        button3 = KeyboardButton("/go_main")
        keyboard.add(button1,button2,button3)
        return keyboard
    def confirm():
        keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        button1 = KeyboardButton("/confirm_deletion_all_messages")
        button2 = KeyboardButton("/go_main")
        keyboard.add(button1,button2)
        return keyboard

@bot.message_handler(commands=["start", "help","go_main"])
def welcome(message: Message):
    bot.send_message(message.from_user.id, "Привет! Выбери следующие команды:",reply_markup=Keyboard.welcome_keyboard())


@bot.message_handler(commands=["write_message"])
def write(message: Message):
    ans = bot.send_message(message.from_user.id, "Хорошо, вы можете написать сообщение, представьтесь, когда закончите нажмите кнопку 'send'",reply_markup=Keyboard.user_keyboard())
    bot.register_next_step_handler(ans, insert_message)

    
def insert_message(message: Message):
    tab.execute("INSERT INTO user_message VALUES (?,?,?)",(message.from_user.id, message.from_user.username,message.text ))    
    
@bot.message_handler(commands=["send"])
def post(message: Message):
    bot.send_message(message.from_user.id, "Спасибо за сообщение)",reply_markup=Keyboard.main_menu())
    con.commit()

admin_mode = False

@bot.message_handler(commands=['admin'])
def admin_enter(message: Message):
    if admin_mode == True:
        bot.send_message(message.from_user.id, "You admin",reply_markup=Keyboard.admin_keyboard())
    else:
        ans = bot.send_message(message.from_user.id, "Enter admin password",reply_markup=Keyboard.main_menu())
        bot.register_next_step_handler(ans, enter_pass)

def enter_pass(message: Message):
    if str(Admin_params.default_pass) == message.text:
        bot.send_message(message.from_user.id, "ok pass",reply_markup=Keyboard.admin_keyboard())
        global admin_mode
        admin_mode = True
    else:
        bot.send_message(message.from_user.id, "You enter incorrect password")  

@bot.message_handler(commands=["read_messages"])
def read_messages(message: Message):
        if admin_mode == True: 
            count = 0
            while True:
                try:
                    bot.send_message(message.from_user.id, ' '.join(map(str, tab.execute("SELECT id, username, message FROM user_message").fetchall().pop(count))))
                    count +=1
                except:
                    break  
        else:
            bot.send_message(message.from_user.id, "sorry, you are not the admin.")


@bot.message_handler(commands=["delete_all_messages"])
def confirm_delete_all(message: Message):
        if admin_mode == True: 
            tab.execute("DELETE FROM user_message")
            bot.send_message(message.from_user.id, "Danger! All messages will delete!",reply_markup=Keyboard.confirm())
        else:
            bot.send_message(message.from_user.id, "sorry, you are not the admin.")


@bot.message_handler(commands=["confirm_deletion_all_messages"])
def delete_all(message: Message):
        if admin_mode == True: 
            con.commit()
            bot.send_message(message.from_user.id, "all messages was deleted.",reply_markup=Keyboard.admin_keyboard())
        else:
            bot.send_message(message.from_user.id, "sorry, you are not the admin.")


bot.polling(non_stop= True)