import sqlite3
import _mypath


conn = sqlite3.connect("../drinkz.db")
c = conn.cursor()

def ex(query):
    global c
    c.execute(query)

query = "DROP TABLE IF EXISTS mfg_liq"
ex(query)

query = "CREATE TABLE mfg_liq (id INTEGER PRIMARY KEY, mfg varchar(64), liquor varchar(64))"
ex(query)

query = "DROP TABLE IF EXISTS inventory"
ex(query)

query = "CREATE TABLE inventory (ml_id int(10), amount varchar(20))" # so sad amount here is varchar :'(
ex(query)

query = "DROP TABLE IF EXISTS types"
ex(query)

query = "CREATE TABLE types (ml_id int(10), type varchar(64))"
ex(query)

query = "DROP TABLE IF EXISTS recipes"
ex(query)

query = "CREATE TABLE recipes (name varchar(64), type varchar(64), amount varchar(20))"
ex(query)

conn.commit()
conn.close()