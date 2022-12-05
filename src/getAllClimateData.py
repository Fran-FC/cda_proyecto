#!/usr/bin/python3

import sys
import requests
import json
import time 

data = json.load(sys.stdin)

url = "https://opendata.aemet.es/opendata/api/valores/climatologicos/valoresextremos/parametro/P/estacion/"
querystring = {"api_key":"eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmcmFmb2xjbUBnbWFpbC5jb20iLCJqdGkiOiI4YTk5YmU2MS01M2Y3LTQ0MmQtYjJmYS03ODA2NTE3M2Y0MGYiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTU3OTQ1MTc5NCwidXNlcklkIjoiOGE5OWJlNjEtNTNmNy00NDJkLWIyZmEtNzgwNjUxNzNmNDBmIiwicm9sZSI6IiJ9.9-8Pm5gqQ1Gi3ZvLnAAHkLkDGpKeVMT0hdLkZhOcHpQ"}
headers = {
    'cache-control': "no-cache"
    }

filePrefix = "infoTemp"

stationsLeft = []

for estacion in data:
    codigo = estacion["indicativo"]

    url = url + str(codigo)
    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
        resp = json.loads(response.text)
        dataUrl = resp["datos"]
        try:
            # obtener de la respuesta la url que contendrá los datos meteorológicas de dicha estacion
            response = requests.request("GET", dataUrl)
            try:
                f = open(filePrefix+str(codigo), "w")
                f.write(response.text)
            finally:
                f.close()
        except Exception as e2:
            print("No se han podido obtener los datos a partir de la url: ", dataUrl, "\nExcepcion: ", e2)
    except Exception as e1:
        print("No se ha podido obtener la url para obtener los datos de la estacion ", codigo, "\nExcepcion: ", e1)
        stationsLeft.append(codigo)
    url = "https://opendata.aemet.es/opendata/api/valores/climatologicos/valoresextremos/parametro/P/estacion/"

while stationsLeft:  
    stationId = stationsLeft.pop(0)
    url = url + str(stationId)

    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
        resp = json.loads(response.text)
        dataUrl = resp["datos"]
        try:
            # obtener de la respuesta la url que contendrá los datos meteorológicas de dicha estacion
            response = requests.request("GET", dataUrl)
            try:
                f = open(filePrefix+str(stationId), "w")
                f.write(response.text)
            finally:
                f.close()
        except Exception as e2:
            print("No se han podido obtener los datos a partir de la url: ", dataUrl, "\nExcepcion: ", e2)
    except Exception as e1:
        print("No se ha podido obtener la url para obtener los datos de la estacion ", stationId, "\nExcepcion: ", e1)
        stationsLeft.append(stationId)
    url = "https://opendata.aemet.es/opendata/api/valores/climatologicos/valoresextremos/parametro/P/estacion/"
    time.sleep(0.5)
