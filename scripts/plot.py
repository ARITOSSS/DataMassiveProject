import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Lire le CSV
df = pd.read_csv("nom_du_fichier.csv")

# Nettoyer AVG_TIME (enlever 'ms' et convertir en float)
df['AVG_TIME'] = df['AVG_TIME'].astype(str).str.replace('ms','').astype(float)

# Calculer la moyenne et l'écart-type par param
summary = df.groupby('PARAM')['AVG_TIME'].agg(['mean','std']).reset_index()

# Créer le plot avec Seaborn et ajouter les barres d'erreur
plt.figure(figsize=(8,6))
ax = sns.barplot(x='PARAM', y='mean', data=summary, palette='Blues_d')
ax.errorbar(x=range(len(summary)), y=summary['mean'], yerr=summary['std'], fmt='none', c='black', capsize=5)

plt.xlabel('x')
plt.ylabel('y')
plt.title('titre')
plt.tight_layout()
plt.savefig("nom_du_fichier.png")
plt.show()
