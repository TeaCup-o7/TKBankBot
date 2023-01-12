import datetime as dt
#calculate time in seconds until the next hour.


def getTimeDif():
    now = dt.datetime.now()
    date = now.date()

    next = now.hour + 1
    next = dt.datetime.strptime("{} {}:{}:{}".format(dt.datetime.strftime(date,'%Y-%m-%d'), str(next),'00', '00'),'%Y-%m-%d %H:%M:%S')
    dif = next - now
    secs = dif.seconds
    return(secs)

#print(getTimeDif())