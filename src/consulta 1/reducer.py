#!/usr/bin/python3

import sys
import json

maxTemp = 0
oldKey = None
oldCod = None
oldYear = None

# Loop around the data
# It will be in the format key\tval
# Where key is the store name, val is the sale amount
#
# All the sales for a particular store will be presented,
# then the key will change and we'll be dealing with the next store

for line in sys.stdin:
    data_mapped = line.strip().split("\t")
    if len(data_mapped) != 4:
        # Something has gone wrong. Skip this line.
        continue

    thisKey, thisCod, thisTemp, thisYear = data_mapped

    if oldKey and oldKey != thisKey:
        print(oldKey, "\t", oldCod, "\t", maxTemp, "\t", oldYear)
        oldKey = thisKey
        oldCod = thisCod
        oldTemp = thisTemp
        oldYear = thisYear
        maxTemp = 0

    oldKey = thisKey
    
    if float(thisTemp) > float(maxTemp):
        maxTemp = thisTemp
        oldCod = thisCod
        oldYear = thisYear

if oldKey != None:
    print(oldKey, "\t", oldCod, "\t", oldTemp, "\t", oldYear)

