#! /usr/bin/python
import operator
from decimal import *

class Utlagg:
    def __init__(self, name, value, persons):
        self.name = name
        self.value = value
        self.persons = persons

    def __repr__(self):
        return "%s:%s:%s" % (self.name, self.value, self.persons)

def prepare(utlaggs):
    balans = {}
    total = {}
    for ut in utlaggs:
        avg = ut.value / (len(ut.persons) + 1)
        balans[ut.name] = balans.get(ut.name, 0) + (avg*len(ut.persons))
        total[ut.name] = total.get(ut.name, 0) + ut.value
        for p in ut.persons:
            balans[p] = balans.get(p, 0) - avg
    return (balans, total)

def calcOverforing(balans):
    transaksjoner = []
    while(len(balans) > 0):
        sortedBalans = sorted(balans.items(), key=operator.itemgetter(1))[::-1]
#        print sortedBalans
        last = sortedBalans[-1]
        rem = abs(last[1])
        i = 0
        while(rem > 0):
            motagare = sortedBalans[i]
            v = rem
            rem -= motagare[1]
#            print rem
            if rem == 0:
                del balans[motagare[0]]
                del balans[last[0]]
            elif rem < 0:
                balans[motagare[0]] = balans[motagare[0]] - v
                del balans[last[0]]
            else:
                v = motagare[1]
                del balans[motagare[0]]
            transaksjoner.append(Utlagg(last[0], v, motagare[0]))
            i += 1
#            print transaksjoner
    return transaksjoner
    
def calc(utlagg):
    overf = prepare(allaUtlagg)
    print "Utlagg totalt:"
    for n in overf[1]:
        print "%s: %s" % (n, overf[1][n])
    return calcOverforing(overf[0])

if __name__ == "__main__":
    allaUtlagg = []
    while True:
        try:
            line = raw_input()
        except EOFError:
            break
        line = line.split('#')[0].strip()
        if line == '':
            continue
        lineSplit = line.split(":")
        allaUtlagg.append(Utlagg(lineSplit[0], Decimal(lineSplit[1]), lineSplit[2:]))
    
    slutopp = calc(allaUtlagg)
    print "\nOverforingar"
    for s in slutopp:
        print s
