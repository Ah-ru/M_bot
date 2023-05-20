from telebot import TeleBot
from telebot.types import *
from config import token, NEW_PASSWD
import datetime
from Keyboards import Keyboard
from sqlite import SQL_Enter

bot = TeleBot(token)

@bot.message_handler(commands=["start", "help", "go_main"])
def welcome(message: Message):
    bot.send_message(message.from_user.id, "Привет! Выбери следующие команды:", reply_markup = Keyboard.welcome_keyboard())


@bot.callback_query_handler(func=lambda call: call.data == "question")
def write(call: CallbackQuery):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
    ans = bot.send_message(chat_id=call.message.chat.id, text= "Готов принять ваш вопрос)\nНапишите его")
    bot.register_next_step_handler(ans, post)

def post(message: Message):
    if message.text is None or message.text.startswith('/'):
        bot.send_message(message.from_user.id, "Спам и ложные сообщения не записываются в базу.", reply_markup = Keyboard.main_menu())
    else:
        bot.send_message(message.from_user.id, "Спасибо за обращение)\nНажмите /go_main для перехода в главное меню", reply_markup = Keyboard.main_menu())
        SQL_Enter.post(message.from_user.id, message.from_user.username, message.text, message.date)



#admin_part
@bot.message_handler(commands=['admin'])
def admin_enter(message: Message):
    if SQL_Enter.exam_admin(message.from_user.id):
        bot.send_message(message.from_user.id, "Pass\nYou are in the admin panel\nYou can click on buttons in menu", reply_markup = Keyboard.admin_keyboard())
    else:
        ans = bot.send_message(message.from_user.id, "Enter admin password", reply_markup = Keyboard.main_menu())
        bot.register_next_step_handler(ans, enter_pass)
            
            
def enter_pass(message: Message):# ok
    if SQL_Enter.enter_pass(message.from_user.id, message.text):
        bot.send_message(message.from_user.id, "Pass\nYou are in the admin panel\nYou can click on buttons in menu", reply_markup = Keyboard.admin_keyboard())
    else:
        bot.send_message(message.from_user.id, "You enter incorrect password", reply_markup = Keyboard.main_menu())  

@bot.message_handler(commands=["all_commands"])
def read_messages(message: Message):
    if SQL_Enter.exam_admin(message.from_user.id):
        bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)
        bot.delete_message(chat_id=message.chat.id, message_id=message.id - 2)
        bot.send_message(message.from_user.id, "All admin commands:", reply_markup = Keyboard.admin_keyboard())
    else:
        bot.send_message(message.from_user.id, "sorry, you are not the admin.", reply_markup = Keyboard.main_menu())


@bot.message_handler(commands=["settings", "back"])
def read_messages(message: Message):
    if SQL_Enter.exam_admin(message.from_user.id):
        bot.send_message(message.from_user.id, text = "To go to other admin commands click /all_commands\nOr click /go_main to go to main menu", reply_markup = Keyboard.all_commands()) 
        bot.send_message(message.from_user.id, "Setting commands:", reply_markup = Keyboard.new_pass_settings_keyboard())
    else:
        bot.send_message(message.from_user.id, "sorry, you are not the admin.", reply_markup = Keyboard.main_menu())


@bot.callback_query_handler(func=lambda call: call.data == "passwd")
def passwd_button(call: CallbackQuery): #ok
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
    ans = bot.send_message(chat_id=call.message.chat.id, text= f"Real Password =  {SQL_Enter.passwd_button()}\nEnter new password", reply_markup = Keyboard.delete())
    bot.register_next_step_handler(ans, passwd_new)
    

def passwd_new(message : Message):
    bot.send_message(message.from_user.id, text=f"New password = {message.text}\nConfirm password\nClick Yes or No", reply_markup = Keyboard.confirm_keyboard())
    global NEW_PASSWD
    NEW_PASSWD= message.text

@bot.message_handler(commands=["Yes"])#OK
def pass_yes(message: Message):
    if SQL_Enter.exam_admin(message.from_user.id):
        bot.send_message(message.from_user.id, text = f"Password was update, password = {NEW_PASSWD}\nClick '/back' to go to settings\nClick '/go_main' to go to main menu", reply_markup = Keyboard.after_passwd_keyboard())
        SQL_Enter.pass_yes(NEW_PASSWD)
    else:
        bot.send_message(message.from_user.id, "sorry, you are not the admin.", reply_markup = Keyboard.main_menu())
    
@bot.message_handler(commands=["No"])
def pass_no(message: Message):
    if SQL_Enter.exam_admin(message.from_user.id):
        bot.send_message(message.from_user.id, text = "Password wasn't update\nClick '/back' to go to settings\nClick '/go_main' to go to main menu", reply_markup = Keyboard.after_passwd_keyboard())
    else:
        bot.send_message(message.from_user.id, "sorry, you are not the admin.", reply_markup = Keyboard.main_menu())


@bot.message_handler(commands=["read_messages"])
def read_messages(message: Message):
    if SQL_Enter.exam_admin(message.from_user.id):#NO
        count = 0
        while True:
            try:
                db = SQL_Enter.read_messages(count)
                offset = datetime.timedelta(hours=3)
                tz = datetime.timezone(offset, name='МСК')
                local_time = datetime.datetime.fromtimestamp(int(db[2]) , tz=tz).strftime('%d-%m-%Y\nTime: %H:%M:%S') 
                bot.send_message(message.from_user.id, text = f"№ {count}\nDate: {local_time}\nUsername: {db[1]}\nid: {db[0]}\nText:\n{db[3]}")
                count +=1
            except:
                if count == 0:
                    bot.send_message(message.from_user.id, "No messages.")
                break                        
    else:
        bot.send_message(message.from_user.id, "sorry, you are not the admin.", reply_markup = Keyboard.main_menu())


@bot.message_handler(commands=["delete_all_messages"])
def delete_all(message: Message):
    if SQL_Enter.exam_admin(message.from_user.id):
        bot.send_message(message.from_user.id, "Danger! All messages will delete!", reply_markup = Keyboard.confirm())
    else:
        bot.send_message(message.from_user.id, "sorry, you are not the admin.", reply_markup = Keyboard.main_menu())


@bot.message_handler(commands=["confirm_deletion_all_messages"])
def confirm_delete_all(message: Message):
    if SQL_Enter.exam_admin(message.from_user.id):
        SQL_Enter.confirm_delete_all()
        bot.send_message(message.from_user.id, "all messages was deleted.", reply_markup = Keyboard.admin_keyboard())
    else:
        bot.send_message(message.from_user.id, "sorry, you are not the admin.", reply_markup = Keyboard.main_menu())

bot.infinity_polling() 