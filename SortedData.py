import numpy as np 
import pandas as pd
from scipy.spatial import distance
from matplotlib import pyplot as plt

data = pd.read_csv("../input/generated/generated.csv")

#data = pd.read_csv("/home/sinda/Bureau/projet_ir/generated.csv")


#lon=data['LON']
#lat=data['LAT']
#debit=data['PIR']
#lon=np.array(data['LON'])
#lat=np.array(data['LAT'])
#debit=np.array(data['PIR'])
data_sorted=data.sort_values(by=['LON'], ascending=True)
cpdata = np.copy(data_sorted)
lon=[]
lat=[]
debit=[]
for i in range(len(cpdata)):
    lon.append(cpdata[i][0])
    lat.append(cpdata[i][1])
    debit.append(cpdata[i][2])
#print(data['LON'])
#print(lon[0])

def dist(p1,p2):
    dst = distance.euclidean(p1,p2)
    return dst;

clusters=[]
v=0
while (len (lon)!=0 and 87989-v>0): 

    lon_rest=[]
    lat_rest=[]
    debit_rest=[]
    i=0
    debit_max=debit[i]
    p0=(lon[i],lat[i])
    cluster=[]
    cluster.append(p0)
    j=1
    while (debit_max<4000 and j < len(lon)):
        ps=(lon[j],lat[j])
        if (dist(p0,ps)<45):
            cluster.append(ps)
            debit_max+=debit_max+debit[j]
        else:
            lon_rest.append(lon[j])
            lat_rest.append(lat[j])
            debit_rest.append(debit[j])
        j+=1


    for k in range(j,len(lon)):
        lon_rest.append(lon[k])
        lat_rest.append(lat[k])
        debit_rest.append(debit[k])

    v+=len(cluster)
    #print(v)
    lon=lon_rest
    lat=lat_rest
    debit=debit_rest
    clusters.append(cluster)

#Nombre de clusters: 14902 après simulations
#14950 en triant par latitudes decroissant
#14972 en triant par latitudes croissant


print(len(clusters))
