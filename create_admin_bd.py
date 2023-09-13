import sqlite3 as sql

con = sql.connect('admin.db')
with con:
    cur = con.cursor()
    comand = "CREATE TABLE IF NOT EXISTS `paswd` (bd STRING, pasw STRING)"
    cur.execute(comand)
    comand = "CREATE TABLE IF NOT EXISTS `backlog` (chat_id INTEGER, bd STRING)"
    cur.execute(comand)
    con.commit()
