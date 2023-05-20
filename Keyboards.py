from telebot.types import KeyboardButton, InlineKeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, ReplyKeyboardRemove

class Keyboard:
    @staticmethod
    def welcome_keyboard():
        keyboard = InlineKeyboardMarkup(row_width=2)
        return keyboard.add(InlineKeyboardButton(text="Задать вопрос",callback_data = "question"))
    
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
        button2 = KeyboardButton("/all_commands")
        button3 = KeyboardButton("/go_main")
        return keyboard.add(button1, button2, button3)
    
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