import sqlite3 as sql

con = sql.connect('admin.db')
with con:
    cur = con.cursor()
    comand = "CREATE TABLE IF NOT EXISTS `paswd` (bd VARCHAR2, pasw VARCHAR2)"
    cur.execute(comand)
    comand = "CREATE TABLE IF NOT EXISTS `backlog` (chat_id INTEGER, bd VARCHAR2)"
    cur.execute(comand)
    con.commit()
