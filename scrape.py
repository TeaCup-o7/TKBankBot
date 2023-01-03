import requests
from bs4 import BeautifulSoup
import Items
import time

def PullData(nameIn):
    print("Starting HTML scrape for {}.".format(nameIn))
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'}

    user_index = 'http://users.nexustk.com/userfiles/'

    #scrape page
    st = True
    while st == True:
        try:
            user_scrape = requests.get(user_index + "{}.html".format(nameIn), headers = headers)
            code = user_scrape.status_code
        except Exception as err:
            er = type(err)
            if er == requests.exceptions.ConnectionError:
                code = 'Request Connection Error'
                pass
            else:
                continue
        print('Status = code ' + str(code))
        if str(code) == '200':
            st = False
        elif str(code) == '404':
            raise requests.exceptions.HTTPError
        else:
            print('Trying again')
            time.sleep(10)
        
            
    user_soup = BeautifulSoup(user_scrape.content, 'html.parser')
    table = user_soup.find('table')
    table = table.get_text()
    split = table.split('\n')
    try:
        split = split[:split.index('Legend')]
    except Exception as err:
        tp = type(err)
        if tp == ValueError:
            try:
                split = split[:split.index('Copyright Nexon Inc. All rights reserved.')-2]
            except:
                pass
            pass    
    
    i = 0
    while (i < len(split)): #remove any empty spaces
        try:
            split.remove('')
            i = i + 1
        except:
            i = i + 1000
   
    #sort the data
    #find index position of lists
    invIndex = split.index('Inventory list') #index pos of inventory list
    bankIndex = split.index('Deposit list') #index pos of deposit list
    invItems = split[invIndex+2:bankIndex] #returns just inventory items
    invGold = split[invIndex+1].split(" ")[1] #returns just inventory gold
    bankItems = split[bankIndex+2:] #returns bank items
    bankGold = split[bankIndex+1].split(" ")[1] #returns bank gold

    #totals
    totalGold = int(bankGold) + int(invGold) #returns total gold
    totalItems = invItems + bankItems #full list of items not sorted any way
    
    dicItems = {} #prepare to create dictionary of items, no duplicates
    for item in totalItems:
        split = item.split('(') #"item ", "#)"
        if len(split) > 1: #if the item had (#)
            splitItem = split[0][:len(split[0])-1] #remove space after item because split at (
            splitQty = split[1].split(')')[0] #gets the qty only
            splitQty = int(splitQty.replace(',',''))
        elif len(split) == 1: #items with no (#)
            splitItem = split[0]
            splitQty = 1
        if splitItem not in dicItems: #if its not in index its added
            dicItems[splitItem] = splitQty
        else:
            dicItems[splitItem] = dicItems[splitItem] + splitQty #if in index its added to the total
    onhands = Items.Items()
    onhands.setOnHands(nameIn, totalGold, dicItems) #create object to hold onhand values
    print("End scrape")
    return(onhands)

#try:
#    PullData('Sajuuk')
#except Exception as er:
#    print(er)
    