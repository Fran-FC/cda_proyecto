#!/usr/bin/python3

import sys
import requests
import json
import time 

# data = json.load(sys.stdin)
data = None
with open("dataset/allStations", "r") as f:
    data = json.loads(f.read())

url = "https://opendata.aemet.es/opendata/api/valores/climatologicos/valoresextremos/parametro/{}/estacion/{}"

querystring = {
    "api_key":"eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmcmFmb2xjbUBnbWFpbC5jb20iLCJqdGkiOiI5YmEwNGI3Yy1lMDY5LTQxYzMtOTU4OC1iY2Q4ZWVhNzMwZmUiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTY3MDI2OTY0NiwidXNlcklkIjoiOWJhMDRiN2MtZTA2OS00MWMzLTk1ODgtYmNkOGVlYTczMGZlIiwicm9sZSI6IiJ9.HkxTYnW4TR_stjkKIgdNocU7pSRxTHn_r4dmK2T09F8"
}

headers = {
    'cache-control': "no-cache"
}

fileTemp = "dataset/infoTemp"

stationsLeft = []
data_stations = []

for property in ["P", "V"]:
    for estacion in data:
        success = False
        while(not success):
            success = True
            time.sleep(0.5)
            indicativo = estacion["indicativo"]

            try:
                resp = requests.request("GET", url.format(property, indicativo), headers=headers, params=querystring)

                json_resp = json.loads(resp.text)
                dataUrl = json_resp["datos"]

                # obtener de la respuesta la url que contendrá los datos meteorológicas de dicha estacion
                response = requests.request("GET", dataUrl)
                json_resp = json.loads(response.text)
                with open(fileTemp, "r") as fr:
                    data_json = json.loads(fr.read())

                    station = [a for a in data_json if a["indicativo"] == indicativo].pop()
                    for key in json_resp:
                        station[key] = json_resp[key]
                
                    data_stations.append(station)
                print("Added {} to {} to data set".format(property, indicativo))
                    
            except Exception as e1:
                print("No se ha podido obtener la url para obtener los datos de la estacion ", indicativo, "\nExcepcion: ", e1)
                success = False
                time.sleep(5)
                continue
            

with open(fileTemp+"2", "w") as fw:
    fw.write(json.dumps(data_stations))
