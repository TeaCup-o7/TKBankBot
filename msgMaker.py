from operator import itemgetter

def createMsg(ob):
    ob.sendMsg = "```diff\n~{}\'s Update~".format(ob.char)
    plusItem = []
    minusItem = []
    g = False
    if ob.difGold > 0:
        ob.sendMsg = ob.sendMsg + "\n+ Gold: +{:,} (New Total: {:,})".format(int(ob.difGold), int(ob.goldNewOnhand))
        g = True
    if ob.difGold < 0:
        ob.sendMsg = ob.sendMsg + "\n- Gold: {:,} (New Total: {:,})".format(int(ob.difGold), int(ob.goldNewOnhand))
        g = True
    #dash if gold + items
    if g == True and (len(plusItem) > 0 or len(minusItem) > 0):
        ob.sendMsg = ob.sendMsg + "\n---------------------------------"
    #items
    for x in ob.difListReport: ##name, new qty, old qty, difference
        item = x[0]
        newQty = str(x[1])
        oldQty = str(x[2])
        dif = x[3]
        if dif > 0:
            plusItem.append((item, "\n+ {}: +{} (New Total: {})".format(item, int(dif), newQty)))
        if dif < 0:
            minusItem.append((item, "\n- {}: {} (New Total: {})".format(item, int(dif), newQty))) #the dif will be negative
    
    sorted(plusItem, key=itemgetter(0))
    sorted(minusItem, key=itemgetter(0))

    for x in plusItem:
        ob.sendMsg = ob.sendMsg + x[1]
    if len(plusItem) != 0:
        ob.sendMsg = ob.sendMsg + '\n'
    for x in minusItem:
        ob.sendMsg = ob.sendMsg + x[1]
    ob.sendMsg = ob.sendMsg + '```'
    
    
    
