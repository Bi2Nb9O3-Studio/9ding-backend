import sqlite3
import os
import threading

class Connection():
    def __init__(self, path, lock: threading.Lock):
        self.path = path
        self.lock = lock
        self.connection = None

    def __enter__(self):
        self.lock.acquire()
        self.connection = sqlite3.connect(self.path)
        return self.connection, self.connection.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.connection.close()
        self.lock.release()


class Database():
    def __init__(self, path):
        self.path = path
        self.lock = threading.Lock()
    def connect(self):
        return Connection(self.path, self.lock)
    def init(self):
        with self.connect() as (con, cur):
            #images
            cur.execute(
                "CREATE TABLE IF NOT EXISTS images (id INTEGER PRIMARY KEY AUTOINCREMENT, author TEXT, name TEXT, category TEXT, teacher TEXT, image TEXT)"
            )
            #config-history
            cur.execute(
                "CREATE TABLE IF NOT EXISTS cfg_history (id INTEGER PRIMARY KEY AUTOINCREMENT, cid INTEGER, data TEXT, time TEXT)"
            )
            cur.execute(
                "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)"
            )
            #insert default user if note exists
            cur.execute(
                f"INSERT OR IGNORE INTO users values (1, 'admin', 'e60da41b2603a837ac93532e4cc11a68f99b8209e8fdd5b7643a9ebc5028784e')"
            )


os.makedirs("./database/", exist_ok=True)
db = Database("./database.db")
db.init()