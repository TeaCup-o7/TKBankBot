#2:13 7/14/23

import pandas as pd
import sqlite3 as sql
from datetime import datetime as dt
import dbm
import matplotlib.pyplot as mp
import platform
from datetime import timedelta as td

#gold_log (gl_char TEXT, gl_gold TEXT, gl_date TEXT)
#gl_char references g_char

def main():
    tester = getLastRecord() #false means last month is different than this month
    print('tester='+str(tester))
    if tester == (True):
        charList = dbm.getPeople()
        for char in charList:
            charName = char[0]
            buildGraph(charName)
        updateLastRecord() #last thing to do once all script has been run and updated
        return(True) #new graphs were created. True will cause the graphs to be uploaded to the rel discord channel
    else:
        return(False) #no graphs created.

def connect():
    sy = platform.system() #changes path to database depending on system type
    if sy == 'Windows':
        db = 'Inv.db' #location of windows db file (same as script folder)
    else:
        db = '/home/pi/Desktop/BankerBot2/Inv.db' #location of the pi's db file
    con = sql.connect(db)
    return(con)

def getDateFormat():
    format = '%Y-%m-%d'
    return(format)

#this is a run condition, if the months do not match we run the script to create graphs
def getLastRecord() -> bool: #checks the last record date vs today and returns bool
    con = connect()
    lastDate = con.execute('''SELECT gl_date FROM gold_log ORDER BY gl_date DESC LIMIT 1''')
    lastDate = lastDate.fetchone()[0]
    lastDate = dt.strptime(lastDate, getDateFormat())
    now = dt.now()
    now = now #+ td(days=18)
    record = con.execute('''SELECT * FROM run_record ORDER BY rr_lastDate DESC LIMIT 1''')
    record = record.fetchall()
    
    if len(record) == 0:
        record = dt.strptime('2001-01-01', getDateFormat())
    else:
        record = record[0][0]
        record = dt.strptime(record, getDateFormat())
    if (record.month != now.month):
        record = True
    else:
        record = False
    
    #print(now.month != lastDate.month) #this is TRUE if this month is different than last month
    con.close()
    return(((now.month != lastDate.month) and record))


def buildGraph(char):
    con = connect()
    data = con.execute('''SELECT * FROM gold_log WHERE gl_char = ?''', (char,))
    data = data.fetchall()
    data = pd.DataFrame(data, columns= ['Name', 'Gold', 'Date'])
    dateMask = pd.to_datetime(data['Date'])
    startDate = dt.today() - td(days=1)
    startDate = dt(year= startDate.year, month=startDate.month, day=1)
    endDate = dateMask[len(dateMask)-1] #last record date
    mask = (dateMask >= startDate) & (dateMask < endDate)
    data = data.loc[mask]
    data = data.reset_index()
    data = data.drop(columns=['index', 'Name'])
    try:
        startGoldIndex = data.iloc[0]
        endGoldIndex = data.iloc[len(data)-1]
        startGold = startGoldIndex['Gold']
        startDate = startGoldIndex['Date']
        endGold = endGoldIndex['Gold']
        endDate = endGoldIndex['Date']
        dif = int(endGold)-int(startGold)
    except Exception as err:
        print(err)
    
    try:
        if (pd.to_numeric(data['Gold']).mean() != pd.to_numeric(data['Gold']).max() 
        and pd.to_numeric(data['Gold']).mean != pd.to_numeric(data['Gold']).min()):
            fix, ax = mp.subplots()
            line = ax.plot(data['Date'], pd.to_numeric(data['Gold']), color='gold', linewidth=2.5)
            mp.figtext(x=0.05, y=0.09, transform=ax.transAxes, fontsize=9,
                   s='Start Gold: {:,} \nEnd Gold: {:,} \nDifference: {:,}'.format(int(startGold), int(endGold), int(dif)),
                   bbox=dict(facecolor='gold', alpha=0.5))
            ax.set_xlabel('Date', fontweight='bold')
            ax.set_ylabel('Gold', fontweight='bold')
            ax.ticklabel_format(axis='y', style='plain', useOffset=False) 
            mp.title(label='Daily Ending Gold Balance: {} \n{} to {}\nGenerated {} {}'.format(char, startDate, endDate, dt.strftime(dt.now(),'{} at %H:%M:%S'.format(getDateFormat())), 'CST'), fontweight='bold')
            mp.setp(ax.get_xticklabels(), rotation=60, horizontalalignment='right', fontsize='x-small')
            mp.savefig('/home/pi/Desktop/BankerBot2/TempGraphs/{}.png'.format(char),
                   pad_inches=0.2,
                   bbox_inches='tight',
                   dpi=256)
            #mp.show()
    except ValueError as err:
        print(err)
    

    #print(data)


#update the last time the script was ran -- only run once a month
def updateLastRecord():
    con = connect()
    now = dt.strftime(dt.now(), getDateFormat())
    #now = '2023-01-01'
    print('{} is the current date that would have been inserted into the table.'.format(now))
    con.execute('''INSERT INTO run_record VALUES (?)''',(now,))
    con.commit()
    con.close()

def addTable(): #need to check when last report was done. only once a month for previous month
    con = connect()
    con.execute('''CREATE TABLE IF NOT EXISTS run_record
                (rr_lastDate TEXT)''')
    print('Table created.')
    con.close()

#create database table

def deleteTable():
    con = connect()
    con.execute('''DROP TABLE IF EXISTS run_record''')
    print('Table dropped')
    con.close()

def selectTest():
    con = connect()
    q = con.execute('''SELECT * FROM gold_log''')
    q = q.fetchall()
    print(q)
    con.close()

#deleteTable()
addTable()
#updateLastRecord()
print(getLastRecord())

#print(selectTest())

#print(main())
#selectTest()

#updateLastRecord()
#test()

#addTable()
#getLastRecord()
