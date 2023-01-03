import dbm
class Items:
    def __init__(self):
        self.char = None
        self.goldNewOnhand = None
        self.itemsNewOnhand = []
        self.goldOldOnhand = None
        self.itemsOldOnhand = []
        self.difGold = 0
        self.difList = []
        self.difListReport = []
        self.itemsOldOnhand = {}
        self.sendMsg = ''

    def setOnHands(self, char, newGold, newDic):
        self.char = char
        self.goldNewOnhand = newGold
        self.itemsNewOnhand = newDic
        self.goldOldOnhand = dbm.getGold(char)
        self.oldOnhand = dbm.getItem(char)
        for x in self.oldOnhand:
            self.itemsOldOnhand[x[1]] = int(x[2])

    def setGoldDif(self, goldDif):
        self.difGold = goldDif

    def setDifList(self, difList):
        
        for x in difList:
            self.difList.append(x)


    

    

    
