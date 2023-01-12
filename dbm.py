
import platform
import sqlite3 as sql
import datetime as dt

#ddl and dml

sy = platform.system() #changes path to database depending on system type

if sy == 'Windows':
    db = 'Inv.db' #location of windows db file (same as script folder)
else:
    db = '/home/pi/Desktop/BankerBot2/Inv.db' #location of the pi's db file


def getNow():
    atm = dt.now()
    date = dt.datetime.strftime(atm, '%Y-%m-%d')
    return(date)

def createDB():
    con = sql.connect(db)

    con.execute('''CREATE TABLE IF NOT EXISTS gold
    (g_char TEXT UNIQUE PRIMARY KEY, 
    g_gold TEXT)''')

    con.execute('''CREATE TABLE IF NOT EXISTS gold_log
    (gl_char TEXT,
    gl_gold TEXT,
    gl_date TEXT,
    FOREIGN KEY (gl_char) REFERENCES gold (g_char))''')

    con.execute('''CREATE TABLE IF NOT EXISTS items
    (i_char TEXT,
    i_item TEXT,
    i_qty TEXT,
    FOREIGN KEY (i_char) REFERENCES gold (g_char))''')

    con.commit()
    con.close()

createDB()

def setGold(gold, char):
    con = sql.connect(db)
    cur = con.cursor()
    try:
        cur.execute('''INSERT INTO GOLD (g_char, g_gold) VALUES (?, ?)''', (char, str(gold)))
    except:
        cur.execute('''UPDATE gold SET g_gold = ? where g_char = ?''', (str(gold),char))        
    con.commit()
    con.close()


def getGold(char):
    con = sql.connect(db)
    cur = con.cursor()
    query = cur.execute('''SELECT g_gold FROM gold WHERE g_char = ?''', (char,))
    cont = []
    for x in query:
        cont.append(x[0])
    con.close()
    try:
        gold = cont[0]
    except:
        setGold(char, '0')
        gold = 0
    return(int(gold))

def setItem(item, qty, char):
    con = sql.connect(db)
    cur = con.cursor()
    try: 
        con.execute('''INSERT INTO items (i_char, i_item, i_qty) VALUES (?, ?, ?)''', (char, item, str(qty))) 
        #print('{} set to {} for {}'.format(item, qty, char))
        con.commit()
    except:
        cur.execute('''UPDATE items SET i_qty = ? where i_char = ? AND i_char = ?''', (qty, item, char))
        #print('{} updated to {} for {}'.format(item, qty, char))
        con.commit()
    con.close()

def getItem(char):
    con = sql.connect(db)
    cur = con.cursor()
    query = cur.execute('''SELECT * FROM items WHERE i_char = ?''',(char,))
    cont = []
    for x in query:
        cont.append(x)
    con.close()
    return(cont)

def removeItem(item, char):
    con = sql.connect(db)
    cur = con.cursor()
    con.execute("DELETE FROM items WHERE i_item = ? and i_char = ?", (item, char))
    print('removed')
    con.commit()
    con.close()

def getAllDB():
    con = sql.connect(db)
    cur = con.cursor()
    query = cur.execute('''select * from items where i_char = ? order by i_item''', ('Sajuuk',))
    cont = []
    for x in query:
        cont.append(x)
    con.close()
    return(cont)

def getPeople():
    con = sql.connect(db)
    cur = con.cursor()
    query = cur.execute('''SELECT * FROM gold''')
    cont = []
    for x in query:
        cont.append(x)
    con.close()
    return(cont)

#for p in getPeople():
#    print(p)

#for x in getAllDB():
#    print(x)


def setGoldLog(char, gold):
    con = sql.connect(db)
    con.execute('''INSERT INTO gold_log (gl_char, gl_gold, gl_date) VALUES (?, ?)''', (char, str(gold), getNow())) 
    con.ccommit()
    con.close()


#removeItem('Shamrock star baloom', 'Barter')
#setItem('Fine metal', 69, 'Barter')
#setItem('World Shout', 99, 'Barter')
#setGold('5000', 'Barter')
#print(getGold('Barter'))
#getAllDB()

#removeItem('Fine metal')
#removeItem('Test Item 2')
#setGold(5)
#setItem('Does not exist', '14')
#setItem('Antique Royal seal', '2')
#setItem('Chung ryong helm', '0')
#setItem('Azure silk', '1')
#setItem('Magical parchment', '922')
#setItem('Fox charm', '9222')



#print(getItem('Barter'))
