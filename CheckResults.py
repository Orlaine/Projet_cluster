#%%
from operator import length_hint
import numpy as np 
import pandas as pd
from scipy.spatial import distance
from matplotlib import pyplot as plt
import ast
from math import sin, cos, sqrt, atan2, radians
import time
import csv

#data = pd.read_csv("IterativeCSV.csv", header=None).T
data = pd.read_csv("NaiveCSV", header=None).T

liste_points = []
#print(data)
#print(liste_copie)
print(len(data))
print(data[0])
liste_points=[] # Tableau de pts
print(data)

for i in range(len(data)):
    cluster=ast.literal_eval(data[0][i])
    liste_points.append(cluster)

debit_MAX=4000000

#Distance entre 2 points
def dist(center,i,point):
    R = 6373.0
    lat1 = radians(center[1])
    lon1 = radians(center[0])
    lat2 = radians(point[i][1])
    lon2 = radians(point[i][0])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c  
    #print(distance)  
    return distance

count = 0
print("longueur liste", len(liste_points))
print("longueur liste 0", len(liste_points[0][0]))
for i in range(len(liste_points)):
    #print(couleur[index])
    #for j in range(len(liste_points)):
    debit_cluster = 0
    for j in range(int(len(liste_points[i]))):
        debit_cluster = debit_cluster + liste_points[i][j][2]
        if (dist(liste_points[i][0], j, liste_points[i])>45):
            print("DISTANCE NON CONFORME", liste_points[i][j][1])
        if (debit_cluster>4000000):
            print("DEBIT NON CONFORME", debit_cluster)
        count = count + 1
    print("Num cluser : ", i, "Longueur cluster = ",len(liste_points[i]),"Debit cluster = ", debit_cluster)