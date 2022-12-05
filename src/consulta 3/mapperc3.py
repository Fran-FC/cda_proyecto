#!/usr/bin/python3

import sys
import json

data = json.load(sys.stdin)

for estacion in data:
        # Imprimimos la temperatura maxima medi
        temperaturaMaxima = estacion["temMax"]
        provincia = estacion["ubicacion"].replace(u'\xd1', 'n')
        anyoTempMax = estacion["anioMax"]
        #formato: PROVINCIA     CODIGO ESTACION     TEMPERATURA MÁXIMA      AÑO
        temperaturaMaximaGrados = int(temperaturaMaxima[12]) / 10
        print(provincia, "\t", temperaturaMaximaGrados, "\t", anyoTempMax[12])
