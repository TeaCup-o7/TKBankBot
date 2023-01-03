import traceback
import datetime as dt


def getNow():
    date = dt.datetime.now()
    date = dt.datetime.strftime(date, '%h-%d-%Y_%H-%M-%S')


class basicHandler:
    def __init__(self):
        self.date = dt.datetime.now()
        self.date = dt.datetime.strftime(self.date, '%h-%d-%Y_%H-%M-%S')
        f = open('{}{}.txt'.format('BankErrorLog', self.date), 'w')
        f.write(self.date + '\n')
        traceback.print_exc(file=f)
        f.close()

class MessageHandler:
    def __init__(self, name):
        self.date = dt.datetime.now()
        self.date = dt.datetime.strftime(self.date, '%h-%d-%Y_%H-%M-%S')
        f = open('{}{}{}.txt'.format(name, 'ErrorLog', self.date), 'w')
        f.write(self.date + '\n' + name + "\n")
        traceback.print_exc(file=f)
        f.close()