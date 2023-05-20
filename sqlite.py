import sqlite3
from contextlib import closing
from config import database
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
                us_id = ' '.join(map(str, tab.execute("SELECT id FROM user_message").fetchall().pop(count)))
                username = ' '.join(map(str, tab.execute("SELECT username FROM user_message").fetchall().pop(count)))
                date = ' '.join(map(str, tab.execute("SELECT time FROM user_message").fetchall().pop(count)))
                text = ' '.join(map(str, tab.execute("SELECT message FROM user_message").fetchall().pop(count)))
                return us_id, username, date, text

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