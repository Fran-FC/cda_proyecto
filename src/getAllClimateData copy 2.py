#!/usr/bin/python3

import sys
import requests
import json
import time 

# data = json.load(sys.stdin)
data = None
with open("dataset/allStations", "r") as f:
    data = json.loads(f.read())

url_1981 = "https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/1981-01-01T00%3A00%3A00UTC/fechafin/1981-12-31T00%3A00%3A00UTC/estacion/{}"
url_2021 = "https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/2021-01-01T00%3A00%3A00UTC/fechafin/2021-12-31T00%3A00%3A00UTC/estacion/{}"

urls = [url_1981, url_2021]

querystring = {
    "api_key":"eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmcmFmb2xjbUBnbWFpbC5jb20iLCJqdGkiOiI5YmEwNGI3Yy1lMDY5LTQxYzMtOTU4OC1iY2Q4ZWVhNzMwZmUiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTY3MDI2OTY0NiwidXNlcklkIjoiOWJhMDRiN2MtZTA2OS00MWMzLTk1ODgtYmNkOGVlYTczMGZlIiwicm9sZSI6IiJ9.HkxTYnW4TR_stjkKIgdNocU7pSRxTHn_r4dmK2T09F8"
}

headers = {
    'cache-control': "no-cache"
}

error_response_text = '{\n  "descripcion" : "No hay datos que satisfagan esos criterios",\n  "estado" : 404\n}'

fileTemp_1981 = "dataset/info1981"
fileTemp_2021 = "dataset/info2021"
climate_files = [fileTemp_1981, fileTemp_2021]

data_stations = []

temp_medias = 0
temp_maxs = []
temp_mins = []
prec_tot = 0

tmed_anterior = 0
for i in range(1,2,1): # 0: 1981 , 1: 2021
    for estacion in data:
        success = False
        indicativo = estacion["indicativo"]
        while(not success):
            success = True
            time.sleep(0.5)
            try:
                resp = requests.request("GET", urls[i].format(indicativo), headers=headers, params=querystring)
                if resp.text == error_response_text: 
                    break

                json_resp = json.loads(resp.text)
                dataUrl = json_resp["datos"]

                # obtener de la respuesta la url que contendrá los datos meteorológicas de dicha estacion
                response = requests.request("GET", dataUrl)
                json_resp = json.loads(response.text)
                    
                for dia in json_resp:
                    if "tmed" not in dia:
                        temp_medias += tmed_anterior
                    else:
                        tmed = float(dia["tmed"].replace(",", "."))
                        temp_medias += tmed

                        tmed_anterior = tmed
                    
                    if "tmax" not in dia:
                        if len(temp_maxs) == 0:
                            temp_maxs.append(tmed_anterior)
                        else:
                            temp_maxs.append(temp_maxs[len(temp_maxs)-1])
                    else:
                        temp_maxs.append(float(dia["tmax"].replace(",", ".")))

                    if "tmin" not in dia:
                        if len(temp_mins) == 0:
                            temp_mins.append(tmed_anterior)
                        else:
                            temp_mins.append(temp_mins[len(temp_mins)-1])
                    else:
                        temp_mins.append(float(dia["tmin"].replace(",", ".")))

                    if "prec" not in dia or dia["prec"] == "Ip" or dia["prec"] == "Acum":
                        prec = 0.0
                    else:
                        prec = float(dia["prec"].replace(",", "."))
                    prec_tot += prec

                print("Obtenida información de estacion {} del año {}".format(indicativo, i))                    
            except Exception as e1:
                print("No se ha podido obtener la url para obtener los datos de la estacion {}\nExcepcion: {}".format(indicativo, e1))
                success = False
                time.sleep(2)
                continue
        
        if resp.text != error_response_text: 
            info_estacion_año = {
                "indicativo": indicativo,
                "nombre": estacion["nombre"],
                "provincia": estacion["provincia"],
                "latitud": estacion["latitud"],
                "longitud": estacion["longitud"],
                "precTot": prec_tot,
                "tmin": min(temp_mins),
                "tmax": max(temp_maxs),
                "tmed": (temp_medias / len(temp_mins))
            }
            data_stations.append(info_estacion_año)

            temp_medias = 0
            temp_maxs = []
            temp_mins = []
            prec_tot = 0

    with open(climate_files[i], "w") as fw:
        fw.write(json.dumps(data_stations))

    data_stations = []
