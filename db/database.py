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
        lang VARCHAR(10) NOT NULL
    )''')





