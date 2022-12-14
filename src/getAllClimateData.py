#!/usr/bin/python3
import requests
import json
import time 


def is_response_correct(resp):
    if "</html>" in resp:
        return False
    return True

if __name__ == "__main__":
    data = None
    with open("dataset/allStations", "r") as f:
        data = json.loads(f.read())

    year = 2021
    url = "https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/{}-01-01T00%3A00%3A00UTC/fechafin/{}-12-31T00%3A00%3A00UTC/estacion/".format(year, year)

    querystring = {
        "api_key":"eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmcmFmb2xjbUBnbWFpbC5jb20iLCJqdGkiOiI5YmEwNGI3Yy1lMDY5LTQxYzMtOTU4OC1iY2Q4ZWVhNzMwZmUiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTY3MDI2OTY0NiwidXNlcklkIjoiOWJhMDRiN2MtZTA2OS00MWMzLTk1ODgtYmNkOGVlYTczMGZlIiwicm9sZSI6IiJ9.HkxTYnW4TR_stjkKIgdNocU7pSRxTHn_r4dmK2T09F8"
    }

    headers = {
        'cache-control': "no-cache"
    }

    error_response_text = '{\n  "descripcion" : "No hay datos que satisfagan esos criterios",\n  "estado" : 404\n}'

    tmed_anterior = 0
    for estacion in data:
        success = False
        indicativo = estacion["indicativo"]
        while(not success):
            success = True
            time.sleep(0.5)
            try:
                resp = requests.request("GET", url+indicativo, headers=headers, params=querystring)
                if resp.text == error_response_text: 
                    break

                json_resp = json.loads(resp.text)
                dataUrl = json_resp["datos"]

                response = requests.request("GET", dataUrl)

                if not is_response_correct(response.text):
                    raise Exception("Response not correct")
                
                with open("dataset/estaciones/{}/{}".format(year, indicativo), "w") as f:
                    f.write(response.text)

                print("Obtenida información de estacion {} del año {}".format(indicativo, year))                    
            except Exception as e1:
                print("No se ha podido obtener la url para obtener los datos de la estacion {}\nExcepcion: {}".format(indicativo, e1))
                success = False
                time.sleep(2)
                continue