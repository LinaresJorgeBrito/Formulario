import sqlite3

def init_db():
    with sqlite3.connect('app.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS passengers (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        cedula TEXT NOT NULL,
                        nombre TEXT NOT NULL,
                        destino TEXT NOT NULL,
                        precio REAL NOT NULL
                    )''')
        conn.commit()

def get_db():
    conn = sqlite3.connect('app.db')
    return conn
