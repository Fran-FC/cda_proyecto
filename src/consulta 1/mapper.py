#!/usr/bin/python3

import sys
import json

data = json.load(sys.stdin)

for estacion in data:
    # Imprimimos la provincia, el codigo de la estacion meteorologica 
    provincia = estacion["ubicacion"]
    codigo = estacion["indicativo"]

    print(provincia, "\t", codigo)
