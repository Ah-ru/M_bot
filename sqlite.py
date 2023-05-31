import sqlite3
import datetime
from contextlib import closing
from config import database

with closing(sqlite3.connect(database)) as con:
    with closing(con.cursor()) as tab:
        try:
            tab.execute("CREATE TABLE admin (id INTEGER, password TEXT)")
            tab.execute("CREATE TABLE bot_params (real_password TEXT, about TEXT, root TEXT)")
            tab.execute("CREATE TABLE ban (id INTEGER)")
            tab.execute("CREATE TABLE user_message (id INTEGER, username TEXT, message TEXT, time INTEGER)")
            tab.execute("INSERT INTO bot_params VALUES (?,?,?)",('0000', '', ''))
            con.commit()
        except sqlite3.OperationalError:
            pass

class SQL_Enter:
    def exam_admin(admin_id):
        with closing(sqlite3.connect(database)) as con:
            with closing(con.cursor()) as tab:
                passwd = ' '.join(map(str, tab.execute("SELECT real_password FROM bot_params").fetchall().pop()))
                try:     
                    admin_passwd = ' '.join(map(str, tab.execute("SELECT password FROM admin WHERE id = (?) ", (admin_id,)).fetchall().pop()))
                except:
                    admin_passwd = ' '
                if passwd == admin_passwd:
                    return True
                else:
                    return False
                
    def read_messages(count):
        with closing(sqlite3.connect(database)) as con:
            with closing(con.cursor()) as tab:
                range_tab = int(' '.join(map(str, tab.execute("SELECT COUNT(*) FROM user_message").fetchall().pop(0))))
                us_id = ' '.join(map(str, tab.execute("SELECT id FROM user_message").fetchall().pop(count)))
                username = ' '.join(map(str, tab.execute("SELECT username FROM user_message").fetchall().pop(count)))
                date = ' '.join(map(str, tab.execute("SELECT time FROM user_message").fetchall().pop(count)))
                text = ' '.join(map(str, tab.execute("SELECT message FROM user_message").fetchall().pop(count))) 
                offset = datetime.timedelta(hours=3)
                tz = datetime.timezone(offset, name='МСК')
                local_time = datetime.datetime.fromtimestamp(int(date) , tz=tz).strftime('%d-%m-%Y\nTime: %H:%M:%S')
                return us_id, username, local_time, text, range_tab, text

    def check_ban(us_id):
        with closing(sqlite3.connect(database)) as con:
            with closing(con.cursor()) as tab:
                try:
                    ' '.join(map(str, tab.execute("SELECT id FROM ban WHERE id = ?",(us_id,)).fetchall().pop()))
                    return True
                except:
                    return False

    def ban_func(count):
        with closing(sqlite3.connect(database)) as con:
            with closing(con.cursor()) as tab:
                us_id = int(' '.join(map(str, tab.execute("SELECT id FROM user_message").fetchall().pop(count))))
                t = tab.execute("SELECT id FROM ban WHERE id = ?",(us_id,)).fetchall()
                if not t:
                    tab.execute("INSERT INTO ban VALUES (?)",(us_id,))
                    con.commit()
                    return True
                else:
                    tab.execute("DELETE FROM ban WHERE id = ?", (us_id,))
                    con.commit()
                    return False

    def check_on_0():
        with closing(sqlite3.connect(database)) as con:
            with closing(con.cursor()) as tab:
                range_tab = int(' '.join(map(str, tab.execute("SELECT COUNT(*) FROM user_message").fetchall().pop(0))))
                if range_tab == 0:
                    return True    
                else:
                    return False

    def post(id, username, text, date):
        with closing(sqlite3.connect(database)) as con:
            with closing(con.cursor()) as tab:
                tab.execute("INSERT INTO user_message VALUES (?,?,?,?)", (id, username, text, date))    
                con.commit()

    def enter_pass(admin_id, n_p):
        with closing(sqlite3.connect(database)) as con:
            with closing(con.cursor()) as tab:
                passwd = ' '.join(map(str, tab.execute("SELECT real_password FROM bot_params").fetchall().pop()))
                if passwd == n_p:
                    tab.execute("DELETE FROM admin WHERE id = (?)", (admin_id,))
                    tab.execute("INSERT INTO admin VALUES (?,?)", (admin_id, passwd))
                    con.commit()
                    return True
                else:
                    return False

    def passwd_button():
        with closing(sqlite3.connect(database)) as con:
            with closing(con.cursor()) as tab:
                return ' '.join(map(str, tab.execute("SELECT real_password FROM bot_params").fetchall().pop()))

    def pass_yes(new_passwd):
        with closing(sqlite3.connect(database)) as con:
            with closing(con.cursor()) as tab:
                tab.execute(f"UPDATE bot_params SET real_password = ('{new_passwd}')")
                con.commit()

    def confirm_delete_all():
        with closing(sqlite3.connect(database)) as con:
            with closing(con.cursor()) as tab:
                tab.execute("DELETE FROM user_message")
                con.commit()
    def send_to_chanel(count):
        with closing(sqlite3.connect(database)) as con:
            with closing(con.cursor()) as tab:        
                text = ' '.join(map(str, tab.execute("SELECT message FROM user_message").fetchall().pop(count)))
                us_id = ' '.join(map(str, tab.execute("SELECT id FROM user_message").fetchall().pop(count)))
                tab.execute("DELETE FROM user_message WHERE id = ?",(us_id,))
                con.commit()
                return text
            
    def delete_message(n):
        with closing(sqlite3.connect(database)) as con:
            with closing(con.cursor()) as tab:
                us_id = ' '.join(map(str, tab.execute("SELECT id FROM user_message").fetchall().pop(int(n))))
                tab.execute("DELETE FROM user_message WHERE id = ?",(us_id,))
                con.commit()