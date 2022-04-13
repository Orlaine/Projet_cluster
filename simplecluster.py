import numpy as np 
import pandas as pd
from scipy.spatial import distance
from matplotlib import pyplot as plt

data = pd.read_csv("generated.csv")
#print(data.head()) # head() method returns top n rows of a DataFrame  with n=5 is default

#data.plot.scatter(x='LON',y='LAT') #Points sur le graphe

#plt.scatter(LAT['LAT'], LON['LON'])

#Initialisations

lon=data['LON']
lat=data['LAT']
debit=data['PIR']
num_cluster=0
liste_points=[] # Tableau de pts
test=[]
centres=[]
clusters=[]
indices_drop=[]
debit_MAX=500000 



#On crée le tableau de points et on crée une copie de ce tableau
for i in range(len(lon)):
    point=[lon[i], lat[i],debit[i],num_cluster]
    liste_points.append(point)
liste_copie = liste_points.copy()
print(len(liste_copie))
print(len(liste_points))
#print(liste_copie[1])

#print(liste_copie[0])



#Distance entre 2 points
def dist(i,j,liste):
    p1=np.array((liste[i][0],liste[i][1]))
    p2=np.array((liste[j][0],liste[j][1]))
    #print(p1)
    #print(p2)
    dst = distance.euclidean(p1,p2)
    #print("distande entre les 2 points")
    #print(dst)
    return dst;
#print(dist(1,2))

#Début de l'algo
num_cluster=1


while (len(liste_copie)>0): #Tant que la liste n'est pas vide

    centres.append(liste_copie[0]) #On initialise/choisis le centre du cluster
    d=0 #initialisation debit cluster 
    count=0
    nb_pts_drop=0
    while(count<len(liste_copie)):
            d=0
            print(count)
            print(len(liste_copie))
            if dist(0,count,liste_copie)<45 :
                print("true")
                d=d+liste_copie[count][2]
                if (d<debit_MAX):
                    liste_points[count+nb_pts_drop][3]=num_cluster
                    liste_copie[count][3]=num_cluster
                    clusters.append(liste_copie[count])
                    indices_drop.append(count)
                    nb_pts_drop+=1
            for k in range(len(indices_drop)):
                del liste_copie[indices_drop[k]]
            count = count + 1
            indices_drop.clear()
            num_cluster+=1

print(clusters)
print("Nombre de clusters ",len(clusters[0]))
print("Nombre de centre",len(centres))