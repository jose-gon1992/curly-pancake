from multiprocessing import connection
import sqlite3

connection = sqlite3.connect('database.db')

with open('create_user_table.sql') as f:
    connection.executescript(f.read())

connection.commit()
connection.close()