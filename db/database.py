import sqlite3 as sql


async def sql_connector():
    con = sql.connect('evos.db')
    cur = con.cursor()

    return con, cur


async def create_tables():
    con, cur = await sql_connector()
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        username VARCHAR(100) NOT NULL,
        lang VARCHAR(10)
    )''')



async def add_user(user_id: int, username: str):
    con, cur = await sql_connector()

    user = cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()

    if not user:
        cur.execute("INSERT INTO users (user_id, username) VALUES (?,?)", (user_id, username))
        con.commit()
        return True

    elif not user[3]:
        return True

    return False


async def set_lang(user_id: int, lang: str):
    con, cur = await sql_connector()
    cur.execute("UPDATE users SET lang = ? WHERE user_id = ?", (lang, user_id))
    con.commit()


async def choose_lang_btn(user_id: int):
    con, cur = await sql_connector()

    user_lang = cur.execute("SELECT lang FROM users WHERE user_id = ?", (user_id,)).fetchone()

    return user_lang[0]









