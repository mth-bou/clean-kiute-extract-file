import pandas as pd
import sys
import json
import numpy as np
from progress.bar import Bar

from urllib.request import urlopen

# df1 = liste de tous les prénoms
df1 = pd.read_csv('./prenoms.csv', 'r', delimiter=";", usecols=['prenom', 'genre'], encoding='latin1')

path = sys.argv[1]

# df2 = liste kiute à compléter
df2 = pd.read_csv(path, "r",
                  delimiter=";",
                  usecols=['Nom', 'prenom', 'genre'],
                  encoding='latin1')

df2 = df2.drop_duplicates(subset=['Nom', 'prenom'], keep='first', inplace=False).reset_index(drop=True)

# Mettre en minuscules toutes les colonnes
df1['prenom'] = df1['prenom'].str.capitalize()

# création d'une nouvelle dataframe comprenant uniquement les lignes avec les cellules 'genre' manquantes
missing = df2.loc[df2['genre'].isna()]

# Suppression des lignes dont les prénoms ou les noms sont inférieurs à 3 caractères
indexNames = df2[len(df2['prenom']) < 3 or len(df2['nom'])].index
df2.drop(indexNames, inplace=True)

bar = Bar('Processing', max=len(df2.index))
for index2 in df2.index:
    p2 = df2['prenom'][index2]
    g2 = df2['genre'][index2]
    for index in df1.index:
        p = df1['prenom'][index]
        g = df1['genre'][index]
        if np.array_equiv(p, p2):
            df2.at[index2, 'genre'] = g
            print('prenom : ', p2, ' - genre : ', g)
            bar.next()
            break
bar.finish()

new_file = pd.DataFrame(df2, columns=['Nom', 'prenom', 'genre'])

export_csv = new_file.to_csv('resultat.csv', index=False, header=True, encoding='latin1', sep=';')
