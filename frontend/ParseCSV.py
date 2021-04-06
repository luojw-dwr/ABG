import csv
from collections import deque

from .GridGraph import *

def parseGridCSV(path):
    V = deque()
    with open(path, 'r') as f:
        fc = csv.DictReader(f)
        for row in fc:
            name = ""
            X = -1
            Y = -1
            area_dict = dict()
            for k in row:
                value = row[k]
                if k == "name":
                    name = value
                elif k == "X":
                    X = int(value)
                elif k == "Y":
                    Y = int(value)
                else:
                    area_dict[k.upper()] = int(value)
            V.append(GridVertex(name, X, Y, area_dict))
    return GridGraph(V)
