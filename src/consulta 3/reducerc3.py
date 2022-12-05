#!/usr/bin/python3

import sys
import json

maxTemp = None
maxKey = None
maxYear = None

# Loop around the data
# It will be in the format key\tval
# Where key is the store name, val is the sale amount
#
# All the sales for a particular store will be presented,
# then the key will change and we'll be dealing with the next store

for line in sys.stdin:
    data_mapped = line.strip().split("\t")
    if len(data_mapped) != 3:

# Something has gone wrong. Skip this line.
        continue

    thisKey, thisTemp, thisYear = data_mapped

    if maxKey==None or float(thisTemp) > float(maxTemp):
        maxKey = thisKey
        maxTemp = thisTemp
        maxYear = thisYear

if maxKey != None:
    print(maxKey, "\t", maxYear, "\t", maxTemp)


