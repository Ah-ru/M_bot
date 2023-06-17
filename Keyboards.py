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
        button2 = KeyboardButton("/settings")
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
        keyboard = InlineKeyboardMarkup(row_width = 1)
        button1 = InlineKeyboardButton(text="Set new password",callback_data = "passwd")
        button2 = InlineKeyboardButton(text="See password",callback_data = "apass")
        return keyboard.add(button1, button2)
    
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
    
    @staticmethod
    def bn():
        keyboard = InlineKeyboardMarkup(row_width=2)
        button1 = InlineKeyboardButton(text="back",callback_data = f"pre")
        button2 = InlineKeyboardButton(text="next",callback_data = f"next")
        return keyboard.add(button1, button2)

    @staticmethod
    def sd(count):
        keyboard = InlineKeyboardMarkup(row_width=3)
        button1 = InlineKeyboardButton(text="send",callback_data = f"add{count}")
        button2 = InlineKeyboardButton(text="ban",callback_data = f"ban{count}")
        button3 = InlineKeyboardButton(text="del",callback_data = f"del{count}")
        return keyboard.add(button1, button2, button3)
