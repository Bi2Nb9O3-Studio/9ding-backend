import sqlite3
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
            cur.execute(
                "CREATE TABLE IF NOT EXISTS images (id INTEGER PRIMARY KEY AUTOINCREMENT, author TEXT, name TEXT, category TEXT, teacher TEXT, image TEXT)")



db = Database("./database.db")
