#!/usr/bin/python3
import json
import statistics

year = 2021

def get_all_values_by_key(key, list):
    res = []
    for l in list:
        if key not in l:
            continue
        val = l[key]
        try:
            val = float(val.replace(",", "."))
        except: 
            val = 0.0
        res.append(val)
    return res


if __name__ == "__main__":
    all_stations = None
    with open("dataset/allStations", "r") as f:
        all_stations = json.loads(f.read())

    climate_file = "dataset/{}_curated".format(year)

    data_stations = []

    for station in all_stations:
        indicativo = station["indicativo"]

        try:
            f = open("dataset/estaciones/{}/{}".format(year, indicativo), "r")  
            info_station = json.loads(f.read())
            
            tmeds = get_all_values_by_key("tmed", info_station)
            tmins = get_all_values_by_key("tmin", info_station)
            tmaxs = get_all_values_by_key("tmax", info_station)
            precs = get_all_values_by_key("prec", info_station)

            info_estacion_año = {
                "indicativo": indicativo,
                "nombre": station["nombre"],
                "provincia": station["provincia"],
                "latitud": station["latitud"],
                "longitud": station["longitud"],
                "precTot": sum(precs),
                "precSD": statistics.pstdev(precs) if precs!=[] else "NA",
                "tMinMed": statistics.mean(tmins) if tmins!=[] else "NA",
                "tMaxMed": statistics.mean(tmaxs)  if tmaxs!=[] else "NA",
                "tMed": statistics.mean(tmeds) if tmeds!=[] else "NA",
                "tMedSD": statistics.pstdev(tmeds) if tmeds!=[] else "NA"
            }
            data_stations.append(info_estacion_año)
        except FileNotFoundError as e:
            print(e)
            continue

            
    with open(climate_file, "w") as fw:
        fw.write(json.dumps(data_stations))
