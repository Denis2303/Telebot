import sqlite3





async def preRegdb(user_id,phoneNum):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users(user_id INT, number INT, password TEXT, discount INT, authorized INT)')

    cur.execute("INSERT INTO users (user_id, number, password, discount, authorized) VALUES (?,?,0,0,0)", (user_id,phoneNum))
    conn.commit()
    conn.close()


async def preUserCarts(user_id):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS userCarts(user_id INT PRIMARY KEY, cartSize INT, pos_1 TEXT)')
    cur.execute("SELECT COUNT(*) FROM userCarts WHERE user_id = ?", (user_id,))
    result = cur.fetchone()[0]
    if result == 0:
        cur.execute('INSERT INTO userCarts (user_id, cartSize, pos_1) VALUES (?,0,?)',(user_id,''))
        conn.commit()