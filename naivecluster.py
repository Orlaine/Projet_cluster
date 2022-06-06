from dis import dis
import numpy as np 
import pandas as pd
from scipy.spatial import distance
from matplotlib import pyplot as plt
import geopy.distance
from math import sin, cos, sqrt, atan2, radians
import time
import csv
data = pd.read_csv("generated.csv")
start_time = time.time()
#print(data.head()) # head() method returns top n rows of a DataFrame  with n=5 is default

#data.plot.scatter(x='LON',y='LAT') #Points sur le graphe

#plt.scatter(LAT['LAT'], LON['LON'])

#Initialisations

lon=data['LON']
lat=data['LAT']
debit=data['PIR']
num_cluster=0
liste_points=[] # Tableau de pts
clusters=[]
debit_MAX=4000000

#On crée le tableau de points et on crée une copie de ce tableau
for i in range(len(lon)):
    point=[lon[i], lat[i],debit[i],num_cluster]
    liste_points.append(point)
liste_copie = liste_points.copy()
print(len(liste_copie))
print(len(liste_points))
longueur = len(liste_copie)
#print(liste_copie[1])
#print(liste_copie[0])

#Distance entre 2 points
def dist2(new_cluster,i,liste):
    R = 6373.0
    lat1 = radians(new_cluster[1])
    lon1 = radians(new_cluster[0])
    lat2 = radians(liste[i][1])
    lon2 = radians(liste[i][0])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c  
    #print(distance)  
    return distance

def dist3(new_cluster,i,liste):
    #Attention: Format du point: [latitude, longitude]
    p1=[new_cluster[1],new_cluster[0]]
    p2=[liste[i][1],liste[i][0]]
    #print(p1,p2)
    return geopy.distance.geodesic(p1,p2).km

def dist(centre_cluster,i,liste):
    p1=[centre_cluster[0],centre_cluster[1]]
    p2=[liste[i][0],liste[i][1]]
    #print(p1)
    #print(p2)
    dst = distance.euclidean(p1,p2)
    #print("distande entre les 2 points")
    #print(dst)
    return dst

#print(dist(1,2))
nb_clusters = 0
#Début de l'algo
while (len(liste_copie)>0): #Tant que la liste n'est pas vide, cad que tous les points n'ont pas été traités
    count = 0 #Indice du traitement de la liste pour le cluster courant
    debit = 0 #Somme des débits du nouveau cluster
    nb_supprime = 0
    new_cluster=[liste_copie[0]] #Nouveau centre d'un cluster
    debit += new_cluster[0][2]
    nb_clusters += 1
    del liste_copie[0] 
    nb_supprime += 1
    while ((count<len(liste_copie)) and debit+50<debit_MAX): #Pour chaque cluster, on cherche à le remplir au maximum. La seconde condition est pour éviter de parcourir inutilement
        if (dist2(new_cluster[0],count-nb_supprime,liste_copie)<45 and (debit+liste_copie[count-nb_supprime][2]<debit_MAX)): #Conditions de distances et de débit
            debit += liste_copie[count-nb_supprime][2]
            new_point_cluster = liste_copie[count-nb_supprime] 
            new_cluster.append(new_point_cluster)
            #print("nb_supprimé ",nb_supprime)
            del liste_copie[count-nb_supprime] #On retire le point ajouté au cluster de la liste
            nb_supprime+=1
        count += 1
    clusters.append(new_cluster)
    #print(new_cluster)
    pourcentage = (longueur-count)/longueur
    print("Count = ", count, "Nb_suppr = ", nb_supprime, "debit du cluster = ", debit, "longueur des centres =", len(clusters),)
    print( "Pourcentage de complétion: ", pourcentage*100,"%", "--- %s seconds ---" % (time.time() - start_time))

#print(clusters)
#print("nb_cluster : ", nb_clusters)
print("Nombre de clusters ",len(clusters[0]))

with open('NaiveCSV', 'w') as f:
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerow(clusters)

#df = pd.DataFrame(clusters).T
#df.to_csv("output.csv")
