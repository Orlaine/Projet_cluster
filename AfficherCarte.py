#%%
from operator import length_hint
import numpy as np 
import pandas as pd
from scipy.spatial import distance
from matplotlib import pyplot as plt
import ast
import mpl_toolkits
mpl_toolkits.__path__.append('/usr/lib/python2.7/dist-packages/mpl_toolkits/')
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
# setup Lambert Conformal basemap.
# set resolution=None to skip processing of boundary datasets.
#m = Basemap(width=12000,height=9000,projection='lcc',
#            resolution=None,lat_1=45.,lat_2=55,lat_0=50,lon_0=-107.)
#m.bluemarble()
#data = pd.read_csv("IterativeCSV2", header=None).T
data = pd.read_csv("Sinda", header=None).T
#data = pd.read_csv("NaiveCSV", header=None).T
#print(data.columns)
#data = data.append(dict(zip(data.columns,['Clusters'])), ignore_index=True)
#print(data)
#read_file = pd.read_csv ('IterativeCSV.csv')
#print(read_file.T)
#read_file.T.to_excel ("test out.xlsx", index = None, header=True)

#data = dat.T
#cen = pd.DataFrame(liste_centres).T
#pd.to_excel("liste_centres_iterative.csv")
#df.to_excel("iterativeoutput2.csv")
liste_points = []
#print(data)
#print(liste_copie)
print(len(data))
#print(data[0])
liste_points=[] # Tableau de pts
#print(data)
test = [2,3,5]
for i in range(len(data)):
    cluster=ast.literal_eval(data[0][i])
    liste_points.append(cluster)
plt.clf()
fig = plt.subplots()

###Liste de couleurs pour l'affichage
couleur = ['tab:grey','tab:brown','tab:orange','tab:olive','tab:green','tab:cyan','tab:cyan','tab:blue','tab:purple','tab:pink','tab:red']
index = 0
len_couleur = len(couleur)
#print(liste_points)
debit_MAX=4000000
ax = plt.gca
#ax.clear()


count = 0
print("longueur liste", len(liste_points))
print("longueur liste 0", len(liste_points[0][0]))
for i in range(int(len(liste_points))):
    #print(couleur[index])
    #for j in range(len(liste_points[i])):
    for j in range(len(liste_points[i])):
        print(i, j, [liste_points[i][j][0],liste_points[i][j][1]], couleur[index])
        if (liste_points[i][j][1]>90):
            print("ANOMALIE", liste_points[i][j][1])
        count = count + 1
        ###On affiche tous les points d'un même cluster avec le même couleur
        
        plt.plot(liste_points[i][j][0],liste_points[i][j][1],marker="o",color = couleur[index],markersize=2)
    circle = plt.Circle((liste_points[i][0][0], liste_points[i][0][1]), 0.64, color=couleur[index], fill=False)
    fig = plt.gcf()
    ax = fig.gca()
    #ax.add_patch(circle)
    ###Changement de cluster=changement de couleur
    index += 1
    index = index%len_couleur
        
print(count,"count")
plt.show()
print("lol")

# %%
