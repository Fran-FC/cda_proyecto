#!/usr/bin/python3

import sys
import requests
import json
import time 

def add_coords_to_station():
    dataset = []
    with open("dataset/allStations", "r") as stations_r:
        with open("dataset/infoStations", "r") as temp_r:
            stations = stations_r.read()
            info_stations = temp_r.read()

            stations_js = json.loads(stations)
            info_stations_js = json.loads(info_stations)

            for s in stations_js:
                for i in info_stations_js:
                    if s["indicativo"] == i["indicativo"]:
                        merged = {**s, **i}
                        dataset.append(merged)
    
        with open("dataset/infoStations", "w") as temp_w:
            temp_w.write(json.dumps(dataset))





def merge_repeated_stations():
    dataset = []
    with open("dataset/infoTemp2", "r") as fr:
        data = fr.read()
        data_json = json.loads(data) 

        codes = list(set([a["indicativo"] for a in data_json if a["indicativo"]]))

        for c in codes:
            s = [a for a in data_json if a["indicativo"] == c]
            merged = {**s[0], **s[1]}
            dataset.append(merged)

        with open("dataset/infoTemp3", "w") as fw:
            fw.write(json.dumps(dataset))

    

if __name__ == "__main__":
    add_coords_to_station()