"""
V 1.6
'Ahsql' is a module written by Ah for the 'Telegram_bot_message_handler' project,"""


import sqlite3
import datetime
from contextlib import closing
from config import database

with closing(sqlite3.connect(database)) as con:#Создание базы данных со всеми таблицами / Create database with all tables
    with closing(con.cursor()) as tab:
        try:
            tab.execute("CREATE TABLE admin (id INTEGER, password TEXT)")
            tab.execute("CREATE TABLE bot_params (real_password TEXT, about TEXT, root TEXT)")
            tab.execute("CREATE TABLE ban (id INTEGER)")
            tab.execute("CREATE TABLE user_message (id INTEGER, username TEXT, message TEXT, time INTEGER)")
            tab.execute("INSERT INTO bot_params VALUES (?,?,?)",('0000', '', ''))
            con.commit()
        except sqlite3.OperationalError:#Проверка, создана ли , создана ли база данных / Checking, database was created or not?
            pass

class SQL_Enter:# Работа с базой дынных / Worked with database
    def exam_admin(admin_id):# Проверка, является ли администратором / Checking on admin, true or false 
        with closing(sqlite3.connect(database)) as con:
            with closing(con.cursor()) as tab:
                passwd = ' '.join(map(str, tab.execute("SELECT real_password FROM bot_params").fetchall().pop()))#Получаем актуальный пароль / get real password
                try:     
                    admin_passwd = ' '.join(map(str, tab.execute("SELECT password FROM admin WHERE id = (?) ", (admin_id,)).fetchall().pop()))#Пробуем получить пароль для конкретного пользователя / try: get password for concrete user
                except IndexError:#Значит пользователя нет в базе / user not in database
                    admin_passwd = ' '# устанавливаем строку / set string 
                if passwd == admin_passwd:#Проверяем, соответствует ли 'админ пароль' актуальному / Checkig, admin password is real password
                    return True
                else:
                    return False
                
    def read_messages(count):
        with closing(sqlite3.connect(database)) as con:
            with closing(con.cursor()) as tab:#{ Получаем данные из базы / get information from database
                range_tab = int(' '.join(map(str, tab.execute("SELECT COUNT(*) FROM user_message").fetchall().pop(0))))
                us_id = ' '.join(map(str, tab.execute("SELECT id FROM user_message").fetchall().pop(count)))
                username = ' '.join(map(str, tab.execute("SELECT username FROM user_message").fetchall().pop(count)))
                date = ' '.join(map(str, tab.execute("SELECT time FROM user_message").fetchall().pop(count)))
                text = ' '.join(map(str, tab.execute("SELECT message FROM user_message").fetchall().pop(count)))#}
                offset = datetime.timedelta(hours=3)# отклонение от UTC / abweichung from UTC 
                tz = datetime.timezone(offset, name='MOS')# Создаем часовой пояс (UTC + 3) / Create timezon (UTC + 3)
                local_time = datetime.datetime.fromtimestamp(int(date) , tz=tz).strftime('%d-%m-%Y\nTime: %H:%M:%S')# переводим UTC в местное время / Translation of UTC to local time
                return us_id, username, local_time, text, range_tab, text

    def range_tab():
        with closing(sqlite3.connect(database)) as con:
            with closing(con.cursor()) as tab:
                return int(' '.join(map(str, tab.execute("SELECT COUNT(*) FROM user_message").fetchall().pop(0))))

    def check_ban(us_id):#Проверка, находится ли пользоватеь в бане / Checking, user are ban-list
        with closing(sqlite3.connect(database)) as con:
            with closing(con.cursor()) as tab:
                try:
                    ' '.join(map(str, tab.execute("SELECT id FROM ban WHERE id = ?",(us_id,)).fetchall().pop()))#Пробуем вернуть id / try: get id 
                    return True
                except IndexError:
                    return False

    def ban_func(count):# Занесение в бан / Insert into ban
        with closing(sqlite3.connect(database)) as con:
            with closing(con.cursor()) as tab:
                us_id = int(' '.join(map(str, tab.execute("SELECT id FROM user_message").fetchall().pop(count))))
                t = tab.execute("SELECT id FROM ban WHERE id = ?",(us_id,)).fetchall()# Пытаемся достать id по id, если успешно, то в списке что-то будет, иначе он буде пуст
                if not t:# Если список пуст:
                    tab.execute("INSERT INTO ban VALUES (?)",(us_id,))
                    con.commit()
                    return True
                else:# Если в списке что-то есть 
                    tab.execute("DELETE FROM ban WHERE id = ?", (us_id,))
                    con.commit()
                    return False

    def check_on_0():# Проверка, остались ли сообщения в базе / Check, there are messages in the database
        with closing(sqlite3.connect(database)) as con:
            with closing(con.cursor()) as tab:
                range_tab = int(' '.join(map(str, tab.execute("SELECT COUNT(*) FROM user_message").fetchall().pop(0))))# Возвращаем количество записей в таблице user_message / get from database, how many messages in database
                if range_tab == 0:
                    return True    
                else:
                    return False

    def post(id, username, text, date):# Запись сообщения пользователя в базу / Insert user message into database
        with closing(sqlite3.connect(database)) as con:
            with closing(con.cursor()) as tab:
                tab.execute("INSERT INTO user_message VALUES (?,?,?,?)", (id, username, text, date))    
                con.commit()

    def enter_pass(admin_id, n_p):# Ввод пароля и проверка его подлинности / Entered the password and checked on the correct
        with closing(sqlite3.connect(database)) as con:
            with closing(con.cursor()) as tab:
                passwd = ' '.join(map(str, tab.execute("SELECT real_password FROM bot_params").fetchall().pop()))
                if passwd == n_p:# Если правда, заносим id и пароль в базу / If correct, insert id and password into database
                    tab.execute("DELETE FROM admin WHERE id = (?)", (admin_id,))
                    tab.execute("INSERT INTO admin VALUES (?,?)", (admin_id, passwd))
                    con.commit()
                    return True
                else:
                    return False

    def passwd_button():# Возвращает текущий 'админ-пароль' / return сurrent admin password
        with closing(sqlite3.connect(database)) as con:
            with closing(con.cursor()) as tab:
                return ' '.join(map(str, tab.execute("SELECT real_password FROM bot_params").fetchall().pop()))

    def pass_yes(new_passwd):# Обновляет 'админ-пароль', которые был получен из переменной 'new_passwd' / Updates the admin password to the password that was given from the 'new_passwd' variable
        with closing(sqlite3.connect(database)) as con:
            with closing(con.cursor()) as tab:
                tab.execute(f"UPDATE bot_params SET real_password = ('{new_passwd}')")
                con.commit()

    def send_to_chanel(count):# Отправка сообщений в канал(Telegram) / Sends message in the Telegram channel
        with closing(sqlite3.connect(database)) as con:
            with closing(con.cursor()) as tab:        
                text = ' '.join(map(str, tab.execute("SELECT message FROM user_message").fetchall().pop(count)))# Получаем сообщение по инвексу / Get message by index
                us_id = ' '.join(map(str, tab.execute("SELECT id FROM user_message").fetchall().pop(count)))
                tab.execute("DELETE FROM user_message WHERE id = ?",(us_id,))# И потом удаляем это сообщение из базы / And then - delete this message from the database
                con.commit()
                return text
            
    def delete_message(n):# Удаление сообщений по индексу /Removes message by index
        with closing(sqlite3.connect(database)) as con:
            with closing(con.cursor()) as tab:
                us_id = ' '.join(map(str, tab.execute("SELECT id FROM user_message").fetchall().pop(int(n))))
                tab.execute("DELETE FROM user_message WHERE id = ?",(us_id,))
                con.commit()