import scrape
import dbm
import pandas
from operator import itemgetter
import exceptionRecorder as er

class jeohwa:
    def __init__(self) -> None:
        self.data = scrape.PullData()
        self.invi = self.data.index('Inventory list') #index pos of inventory list
        self.banki = self.data.index('Deposit list') #index pos of deposit list
        self.inventory = self.data[self.invi+2:self.banki]
        self.invGold = self.data[self.invi+1].split(" ")[1]
        self.deposits = self.data[self.banki+2:]
        self.depGold = self.data[self.banki+1].split(" ")[1]
        self.newGold = int(self.depGold) + int(self.invGold)

class changet:
    def __init__(self, itemNm, oldQty, newQty):
        self.itemNm = itemNm
        self.oldQty = oldQty
        self.newQty = newQty
        self.diff = int(self.newQty) - int(self.oldQty)




class message: #what a fuckin mess i went off the rails on this one prototyping lol oh well
    def __init__(self) -> None:
        self.msg = '```diff\n~Bank update~\n'
        self.jeo = jeohwa()
        self.oldGold = dbm.getGold()
        self.dif = self.jeo.newGold - self.oldGold
        if self.dif == 0:
            self.status = False
        else:
            self.status = True
            dbm.setGold(self.jeo.newGold)
            if self.dif > 0: #'{:,}'.format(value)
                self.msg = self.msg + '+ Gold: +{:,} (New Total: {:,})\n'.format(self.dif, self.jeo.newGold)
            else:
                self.msg = self.msg + '- Gold: {:,} (New Total: {:,})\n' .format(self.dif, self.jeo.newGold)
            #self.msg = self.msg + '------------------------------------------------\n'
        t1 = self.jeo.inventory
        t2 = self.jeo.deposits
        self.items = t1 + t2
        #squish all this into a dictionary
        self.squshed = {}
        for item in self.items:
            try:
                split = item.split('(') #"item ", "#)"
                item = split[0] #item
                if len(split) > 1:
                    item = item[:len(item)-1] #this is suppose to remove the space after item

                qty = split[1][:len(split[1])-1]
                qty = qty.replace(',','')
                try:
                    self.squshed[item] = int(self.squshed[item]) + int(qty)
                except:
                    self.squshed[item] = int(qty)
                    er.basicHandler()
                txt = "Name = {} Qty = {}".format(item, qty)
                #print(txt)
            except:
                txt = "Name = {} Qty = 1".format(item) 
                try:
                    self.squshed[item] = self.squshed[item] + 1
                except:
                    self.squshed[item] = 1
        self.oldItems = dict(dbm.getItem())
        self.newItems = list(self.squshed.copy().items())
        self.difs = []
        self.updateList = []
        self.updateThing = []

        for item in self.oldItems:
            try:
                self.squshed[item] #checks if old item in new list: fails if not in the list = removed
            except: #remove items not found from old list
                thing = changet(item, self.oldItems[item], 0) #pass item name, old qty, new qty
                self.updateThing.append(thing) #saves thing in updateThing
                self.difs.append((item, str(int(self.oldItems[item])*-1))) #this just sets difference to what ever the total was
                dbm.removeItem(item)
                #dif = new qty - old qty

        for item in self.newItems:
            try:
                self.oldQty = self.oldItems[item[0]]
                self.oldQty
                if item[1] == self.oldQty:
                    pass
                    #print('no change in qty')
            except:
                print('except added new item')
                self.updateList.append(item) #this accounts for items that are not in the database yet
                thing = changet(item[0], 0, int(item[1])) #item name, previous qty (0), new qty
                self.updateThing.append(thing)
                self.difs.append(item) #this is putting the right difs
            try: #sorted(decList, key=itemgetter(0))
                if item[0] in list(dict(self.difs)): #list(dic) - lazily grabbing keys to make a list from the list lol
                    pass
                else:
                    self.dif = int(item[1]) - int(self.oldQty) #dif = new qty - old qty
                    thing = changet(item[0], int(self.oldQty), int(item[1]))
            except Exception as err:
                self.dif = 0
            if self.dif != 0:
                print("dif = {}".format(str(self.dif)))
                self.difs.append((item[0], self.dif)) #we will need to put these in the discord output
                self.updateThing.append(thing)
                self.updateList.append(item)
                print('different qty needs to be updated')
                #print('append item {} in the exception section'.format(item))
        for item in self.updateList:
            print('set an item')
            dbm.setItem(item[0], item[1])
        if self.status == True and len(self.updateList) != 0:
            self.msg = self.msg + '------------------------------------------------\n'
        #self.difs
        y = 0
        incList = []
        decList = []
        print(self.difs)
        for x in self.difs:
            print('difference')
            self.status = True #tells bot to send message
            print(x)
            item = x[0]
            change = x[1]
            if int(change) > 0:
                print("+")
                incList.append([item, "+ {}: +{} (New Total = {})\n".format(item, change, str(self.updateThing[y].newQty))])
                #self.msg = self.msg + "+ {} increased by: {} | {} to {}\n".format(item, change, str(self.updateThing[y].oldQty), str(self.updateThing[y].newQty))
            else:
                print("-")
                decList.append([item, "- {}: {} (New Total = {})\n".format(item, change, str(self.updateThing[y].newQty))])
                #self.msg = self.msg + "- {} decreased by: {} | {} to {}\n".format(item, change, str(self.updateThing[y].oldQty), str(self.updateThing[y].newQty))
            y = y + 1
        incList = sorted(incList, key=itemgetter(0))
        decList = sorted(decList, key=itemgetter(0))
        for x in incList:
            self.msg = self.msg + x[1]
        if len(incList) != 0:
            self.msg = self.msg + "\n"
        for x in decList:
            self.msg = self.msg + x[1]
        self.end = self.msg + '```'            




