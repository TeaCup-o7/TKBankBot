import dbm
def main():
    people = dbm.getPeople()
    for per in people:
        person = per[0]
        gold = per[1]
        dbm.setGoldLog(person, gold)
        print(person, gold)

main() #logs the daily gold totals
