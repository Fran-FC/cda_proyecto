#!/usr/bin/python3

import sys
import json

data = json.load(sys.stdin)

for estacion in data:
        # Imprimimos la provincia, el codigo de la estacion meteorologica 
        # y la temperatura maxima media registrada en dicha estacion
        provincia = estacion["ubicacion"].replace(u'\xd1', 'n')
        codigo = estacion["indicativo"]

        temperaturaMaxima = estacion["temMedMax"]
        anyoTempMax = estacion["anioMedMax"]
        #formato: PROVINCIA     CODIGO ESTACION     TEMPERATURA MÁXIMA      AÑO
        temperaturaMaximaGrados = int(temperaturaMaxima[12]) / 10
        print(provincia, "\t", codigo, "\t", temperaturaMaximaGrados, "\t", anyoTempMax[12])
