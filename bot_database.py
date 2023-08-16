import sqlite3
import configparser
import telethon


conn =sqlite3.connect('music.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS songz
               (name TEXT,link TEXT)''')

def insert_data(name,link):
    cursor.execute('''INSERT INTO songz VALUES (?,?) ''',(name,link))
    conn.commit()

def print_data():
    cursor.execute('SELECT * FROM songz')
    mydict = {}
    data=cursor.fetchall()
    mydict.update(data)
    return mydict
def all_v():
    cursor.execute('SELECT *  FROM songz')
    info =cursor.fetchall()
    variable = (dict(info)).values()
    return variable
def all_k():
    cursor.execute('SELECT *  FROM songz')
    info =cursor.fetchall()
    variable = (dict(info)).keys()
    return "\n".join(variable)
def add_song(n):
    cursor.execute('SELECT * FROM songz WHERE name = ?' ,(n,))
    data = cursor.fetchone()
    dic=  dict({n:data})
    x = dic.values()
    newl= list(x)
    new = []
    new.append(newl[0][1])
    return "".join(new)
#print(add_song('porteghale_man'))
#print(add_song() )
print(add_song('lonely'))

#print(print_data())
