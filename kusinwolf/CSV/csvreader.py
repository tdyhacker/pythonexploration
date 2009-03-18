import csv
from datetime import datetime
from re import compile

#randomReader = csv.reader(open('randomdata.csv', 'r'), delimiter='|')
randomReader = csv.reader(open('randomdata2.csv', 'r'), delimiter='|')
csvwriter = csv.writer(open('newrandom.csv', 'w'), delimiter='~')

columns = None
data = []

class Data(object):
    def __init__(self, row):
        r = 0
        for col in columns:
            if compile("[0-9]{2}/[0-9]{2}/[0-9]{2}").match(row[r]):
                date = compile("([0-9]{2})/([0-9]{2})/([0-9]{2})").match(row[r]).groups()
                self.__setattr__(col, datetime(year=int("20" + date[2]), month=int(date[0]), day=int(date[1])))
            else:
                self.__setattr__(col, row[r])
            r += 1
        del r
    
    def __repr__(self):
        values = ""
        names = self.__dict__.keys()
        names.sort()
        for attr in names:
            if values != "":
                values = "%(values)s," % {"values": values}
            values = "%(values)s %(name)s: %(value)s" % {"values": values, "name": attr, "value": self.__dict__[attr]}
        return "<Data%s>" % values

for row in randomReader:
    if columns == None:
        columns = row
    else:
        if len(row):
            csvwriter.writerow(row)
            data.append(Data(row))