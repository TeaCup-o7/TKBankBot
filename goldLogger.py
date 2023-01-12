import dbm
#independant script to run checking the values of gold at the end of each day
#these values will be used to provide an end of month report.
def main():
    people = dbm.getPeople()
    for per in people:
        person = per[0]
        gold = per[1]
        dbm.setGoldLog(person, gold)
        print(person, gold)

main() #logs the daily gold totals
