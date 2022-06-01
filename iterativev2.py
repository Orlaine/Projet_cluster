from operator import length_hint
import numpy as np 
import pandas as pd
from scipy.spatial import distance
from matplotlib import pyplot as plt
import csv
import time
from math import sin, cos, sqrt, atan2, radians
import geopy.distance

data = pd.read_csv("generated.csv")
#print(data.head()) # head() method returns top n rows of a DataFrame  with n=5 is default
start_time = time.time()
#data.plot.scatter(x='LON',y='LAT') #Points sur le graphe

#plt.scatter(LAT['LAT'], LON['LON'])

#Initialisations

lon=data['LON']
lat=data['LAT']
debit=data['PIR']
liste_points=[] # Tableau de pts
clusters=[]
debit_MAX=4000000

########## Dans cette version le premier élément d'un tableau cluster contient le centre du cluster, qui est recalculé de façon
########## à être le barycentre de tous les points du cluster à chaque ajout de point au cluster 

#On crée le tableau de points et on crée une copie de ce tableau
for i in range(int(len(lon))):
    point=[lon[i], lat[i],debit[i]]
    liste_points.append(point)
liste_copie = liste_points.copy()
print(len(liste_copie))
print(len(liste_points))
longueur_liste = len(liste_points)
#print(liste_copie[1])
#print(liste_copie[0])
liste_centres = []
#Distance entre 2 points
def dist(centre_cluster,i,liste):
    #Attention: Format du point: [latitude, longitude]
    p1=[centre_cluster[1],centre_cluster[0]]
    p2=[liste[i][1],liste[i][0]]
    #print(p1,p2)
    return geopy.distance.geodesic(p1,p2)

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
    distance = R * c

    #print(p1,p2)
    #dst = distance.euclidean(p1,p2)
    #print("distande entre les 2 points")
    #print(dst)
    return distance
#print(dist(1,2))
nb_clusters = 0
#Début de l'algo

def calcul_centre(new_cluster):
    abscisse=[]
    ordonnees=[]
    #print("New cluster = ", new_cluster)
    for i in range(len(new_cluster)):
        abscisse.append(new_cluster[i][0])
        ordonnees.append(new_cluster[i][1])
    #print(abscisse,ordonnees)
    new_centre = [np.mean(abscisse), np.mean(ordonnees), 0]
    #print(new_centre)
    return(new_centre)


print("Début du calcul")
while (len(liste_copie)>0): #Tant que la liste n'est pas vide, cad que tous les points n'ont pas été traités
    longueur_init = len(liste_copie)
    count = 1 #Indice du traitement de la liste pour le cluster courant
    debit = 0 #Somme des débits du nouveau cluster
    nb_supprime = 0
    new_cluster=[liste_copie[0]] #Nouveau centre d'un cluster
    #new_cluster.append(liste_copie[0]) #On ajoute le premier point au cluster
    liste_centres.append(liste_copie[0])
    del liste_copie[0]
    debit += new_cluster[0][2]
    nb_clusters += 1
    nb_supprime += 1
    #Pour chaque cluster on cherche une remplissage maximal
    while(count<longueur_init and debit+50<debit_MAX):
        #print("count ", count, "nb suppr ", nb_supprime, "len list ", len(liste_copie))
        distance = dist2(liste_centres[-1],count-nb_supprime,liste_copie)
        if (distance<45) and (debit+liste_copie[count-nb_supprime][2]<debit_MAX):
            #print(liste_centres[-1],liste_copie[count-nb_supprime])
            #print(distance,liste_centres[-1], liste_points[count-nb_supprime])
            new_cluster.append(liste_copie[count-nb_supprime])
            debit = debit + liste_copie[count-nb_supprime][2]
            liste_centres[-1] = calcul_centre(new_cluster)
            #print("New cluster = ",new_cluster)
            del liste_copie[count-nb_supprime]
            nb_supprime = nb_supprime + 1
            #print("Nb supprimé = ", nb_supprime)
        count = count + 1
        #print(count)
    clusters.append(new_cluster)
    pourcentage = (longueur_liste-longueur_init)/longueur_liste
    print("Count = ", count, "Nb_suppr = ", nb_supprime, "debit du cluster = ", debit, "longueur des centres =", len(liste_centres),)
    print( "Pourcentage de complétion: ", pourcentage*100,"%", "--- %s seconds ---" % (time.time() - start_time))


#15h15 38000
#3h24

"""figure, axes = plt.subplots()
draw_circle = plt.Circle((0.5, 0.5), 0.1,fill=False)
axes.set_aspect(1)
axes.add_artist(draw_circle)
plt.show()
"""

#print(clusters)
print("nb_cluster : ", nb_clusters)
print("centres = ", len(liste_centres))
print("Nombre de clusters ",len(clusters))
print("longueur de la liste originale ", len(liste_points))
print("--- %s seconds ---" % (time.time() - start_time))
#df = pd.DataFrame(clusters).T
#cen = pd.DataFrame(liste_centres).T
#cen.to_excel("liste_centres_iterative.csv")
#df.to_excel("iterativeoutput2.csv")

with open('IterativeCSV2', 'w') as f:
      
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerow(clusters)

with open('IterativeCentres2', 'w') as f:
      
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerow(liste_centres)