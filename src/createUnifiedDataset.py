#!/usr/bin/python3

import sys
import json

dataList =[]

for codigo in sys.stdin:
    fileName = "datasets/infoTemp" + str(codigo).replace('\n', '')
    try:
        f = open(fileName, "r")
        data = f.read()
        dataList.append(json.loads(data))
    except Exception as e:
        print("Could not open the file", fileName, "\t", e)
    finally:
        f.close()
    
f = open("infoTemp", "w")
try:
    jsonData = json.dumps(dataList)
    f.write(jsonData)
finally:
    f.close()