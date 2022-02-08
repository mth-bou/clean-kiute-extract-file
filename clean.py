import pandas as pd
import sys
import json
import numpy as np

from urllib.request import urlopen

firstnames_reader = pd.read_csv('./prenoms.csv', 'r', delimiter=";", usecols=['prenom', 'genre'], encoding='latin1')

path = sys.argv[1]

extract_file_reader = pd.read_csv(path, "r",
                                  delimiter=";",
                                  usecols=['prenom', 'genre'],
                                  encoding='latin1')

#extract_file_reader.drop_duplicates(subset=['Nom', 'prenom'], keep='first').reset_index(drop=True)
new_file = pd.DataFrame(extract_file_reader,
                        columns=['Prénom', 'Genre'])

# for name1 in extract_file_reader['Prénom'].str.lower():
#     for name2 in firstnames_reader['prenom']:
#         if name1 == name2:
#             print("   ")


extract_file_reader['Genre déterminé'] = np.where(extract_file_reader['prenom'] == firstnames_reader['prenom'], True, False)

#if pd.isna(extract_file_reader['Genre']):

print(extract_file_reader)
print(firstnames_reader)

export_csv = new_file.to_csv('resultat.csv', index=False, header=True, encoding='utf-8', sep=';')

print(extract_file_reader.reset_index(drop=True).equals(firstnames_reader.reset_index(drop=True)))
