#!/usr/bin/python3

import sys
import json

data = json.load(sys.stdin)

for estacion in data:
        # Imprimimos la temperatura maxima medi
        temperaturaMin = estacion["temMin"]
        provincia = estacion["ubicacion"].replace(u'\xd1', 'n')
        anyoTempMin = estacion["anioMin"]
        #formato: PROVINCIA     CODIGO ESTACION     TEMPERATURA MÁXIMA      AÑO
        temperaturaMinGrados = int(temperaturaMin[12]) / 10
        print(provincia, "\t", temperaturaMinGrados, "\t", anyoTempMin[12])


