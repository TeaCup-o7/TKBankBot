import dbm
import exceptionRecorder as er
import msgMaker as mm

def MainSort(ob):
    try:
        #print('Checking gold difference')
        setGoldDif(ob)
    except:
        er.basicHandler()
    try:
        #print('Checking for new items')
        findNewItems(ob)
    except:
        er.basicHandler()
    try:
        #print('Checking for changed quantites')
        checkQtyChange(ob)
    except:
        er.basicHandler()
    try:
        #print('Checking for items that no longer exist')
        checkNotExisting(ob)
    except:
        er.basicHandler()
    try:
        #print('Reporting differnces')
        reportDifferences(ob)
    except:
        er.basicHandler()
    
    mm.createMsg(ob)

def setGoldDif(ob):
    ob.difGold = int(ob.goldNewOnhand) - int(ob.goldOldOnhand)
    dbm.setGold(str(ob.goldNewOnhand), ob.char)

def findNewItems(ob): #looks for items that don't exist in the database yet
    newDic = ob.itemsNewOnhand
    oldDic = ob.itemsOldOnhand
    newList = list(newDic)
    oldList = list(oldDic)
    for x in newList:
        if x not in oldList:
            qty = newDic[x]
            print("NEW ITEM ADDED {} FOUND #{}".format(x, qty))
            newItem = (x, qty)
            ob.difList.append(newItem) #adds new item to the difference list
            dbm.setItem(x, qty, ob.char) #adds new item to the database
            #ob.difListReport.append((x, qty, 0, qty)) #name, new qty, old qty, difference

    #ob.setDifList(ob, difList)
def checkQtyChange(ob): #checks new qty vs old qty to find changes
    newDic = ob.itemsNewOnhand
    oldDic = ob.itemsOldOnhand
    newList = list(newDic)
    oldList = list(oldDic)
    for x in newList:
        if x in oldList and newDic[x] != oldDic[x]: #looks for existing quantities that change
            qty = newDic[x]
            print("FOUNT NEW QTY {} FOUND #{}".format(x, qty))
            newItem = (x, qty)
            ob.difList.append(newItem)
            dbm.setItem(x, qty, ob.char)

def checkNotExisting(ob): #looks for items that no longer exist.
    newDic = ob.itemsNewOnhand
    oldDic = ob.itemsOldOnhand
    newList = list(newDic)
    oldList = list(oldDic)
    for x in oldList:
        if x not in newList:
            print("THIS ITEM NO LONGER EXISTS {}".format(x))
            delItem = (x, 0)
            ob.difList.append(delItem)
            dbm.removeItem(x, ob.char)

def reportDifferences(ob):
    oldDic = ob.itemsOldOnhand
    oldList = list(oldDic)
    for x in ob.difList:
        item = x[0]
        newQty = x[1] #new qty
        if item in oldList:
            oldQty = oldDic[item]
        else:
            oldQty = 0
        difQty = newQty - oldQty
        ob.difListReport.append((item, newQty, oldQty, difQty))