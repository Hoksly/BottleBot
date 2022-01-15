import sqlite3
from settings import DATABASE_PATH
from translations import UL
from random import randint


def recreate_db():
    con = sqlite3.connect(DATABASE_PATH)
    cur = con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS User(
                ID INT PRIMARY KEY,
                LANGUAGE INT,
                COUNTER INT
                )
    """)

    cur.execute("""CREATE TABLE IF NOT EXISTS Message(
            ID INT PRIMARY KEY,
            TYPE TEXT,
            TELEGRAM_ID TEXT
    )""")

    con.commit()
    con.close()


def add_user(user_id, user_link='@none', lang=0):
    con = sqlite3.connect(DATABASE_PATH)
    cur = con.cursor()
    cur.execute("SELECT LANGUAGE FROM User WHERE ID = ?", (user_id,))
    if not cur.fetchone():
        cur.execute("INSERT INTO User(ID, LANGUAGE, COUNTER) VALUES (?, ?, ?)", (user_id, lang,  0))
    con.commit()
    UL.update({str(user_id):0})
    con.close()


def add_content(content_id: str, content_type: str):
    con = sqlite3.connect(DATABASE_PATH)

    cur = con.cursor()
    cur.execute('SELECT ID FROM Message WHERE TELEGRAM_ID = ?', (content_id,))
    ms = cur.fetchone()
    print(ms)
    if not ms:
        print("HERE")

        print(content_id)
        cur.execute("SELECT MAX(ID) FROM Message")
        mx = cur.fetchone()[0]
        cur.execute("INSERT INTO Message(ID, TELEGRAM_ID, TYPE) VALUES (?, ?, ?)", (mx + 1, content_id, content_type))
        con.commit()
    con.close()


def update_user_language(user_id, new_lang):
    con = sqlite3.connect(DATABASE_PATH)
    cur = con.cursor()
    cur.execute('SELECT COUNTER FROM User WHERE ID = ?', (user_id,))
    l = cur.fetchone()

    if l:
        cur.execute("""UPDATE User SET LANGUAGE = ? WHERE ID = ?""", (new_lang, user_id))

    else:
        add_user(user_id, '@none', new_lang)

    con.commit()
    con.close()


def load_users_languages():
    con = sqlite3.connect(DATABASE_PATH)

    cur = con.cursor()

    cur.execute("""
    SELECT ID, LANGUAGE FROM User
    """)

    users = cur.fetchall()
    for el in users:
        UL.update({str(el[0]): int(el[1])})


def update_user_counter(user_id: int):
    con = sqlite3.connect(DATABASE_PATH)
    cur = con.cursor()
    cur.execute('SELECT COUNTER FROM User WHERE ID = ?', (user_id,))
    if cur.fetchone():
        cur.execute("""UPDATE User SET COUNTER = COUNTER + 1 WHERE ID = ?""", (user_id,))
    else:
        add_user(user_id, '@none', 0)
    con.commit()


def get_random_post():
    con = sqlite3.connect(DATABASE_PATH)
    cur = con.cursor()
    cur.execute("SELECT MAX(ID) FROM Message")

    mx = cur.fetchone()[0]
    cur.execute("SELECT TELEGRAM_ID, TYPE FROM Message WHERE ID = ?", (randint(1, mx),))

    return cur.fetchone()


def load_content():
    # get_random_post is better to use: less usage of memory
    con = sqlite3.connect(DATABASE_PATH)

    cur = con.cursor()

    cur.execute("""SELECT TELEGRAM_ID, TYPE FROM Message""")
    return cur.fetchall()


if __name__ == '__main__':
    recreate_db()
    print(get_random_post())