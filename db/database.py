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


    cur.execute("""CREATE TABLE IF NOT EXISTS category(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name VARCHAR(100) NOT NULL,
            category_img TEXT NOT NULL
        )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS products(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name VARCHAR(100) NOT NULL,
                description TEXT NOT NULL,
                product_price REAL NOT NULL,
                product_img TEXT NOT NULL,
                category_id INTEGER NOT NULL,
                FOREIGN KEY (category_id) REFERENCES category(id) ON DELETE CASCADE
    )""")



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


async def get_user_lang(user_id: int):
    con, cur = await sql_connector()

    user_lang = cur.execute("SELECT lang FROM users WHERE user_id = ?", (user_id,)).fetchone()

    return user_lang[0]


async def get_all_categories():
    con, cur = await sql_connector()

    categories = cur.execute("SELECT * FROM category").fetchall()
    return categories


async def get_products(category: str):
    con, cur = await sql_connector()

    category = cur.execute("SELECT id, category_img FROM category WHERE category_name = ?", (category,)).fetchone()
    products = cur.execute("SELECT * FROM products WHERE category_id = ?", (category[0],)).fetchall()
    return products, category[1]


async def get_product_info(product: str):
    con, cur = await sql_connector()

    products = cur.execute("SELECT * FROM products WHERE product_name = ?", (product,)).fetchone()
    return products
    

