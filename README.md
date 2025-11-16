# DataMassiveProject

## **Passage à l'échelle sur la charge :**


### Génération des données :
Peuplement du Datastore avec 1000 utilisateurs, 50 posts par utilisateur et 20 followees :

```bash
python seed.py --users 1000 --posts 50000 --follows-min 20 --follows-max 20
```

### Benchmark des performances :
Script Python pour mesurer le temps moyen d'une requête timeline pour différentes concurrences et sauvegarder les résultats dans un CSV (conc.csv) :

```bash
import subprocess
import csv
import re

# Paramètres
url = "https://tp1-massive-data.ew.r.appspot.com/api/timeline?user=user1"
concurrences = [1, 10, 20, 50, 100, 1000]
runs = 3
csv_file = "conc.csv"

# Préparer le CSV
with open(csv_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["PARAM","AVG_TIME","RUN","FAILED"])

    for c in concurrences:
        for r in range(1, runs+1):
            print(f"Running: concurrency={c}, run={r}")
            try:
                result = subprocess.run(
                    ["ab", "-n", "100", "-c", str(c), url],
                    capture_output=True, text=True, check=True
                )
                match = re.search(r"Time per request:\s+([\d\.]+) \[ms\]", result.stdout)
                avg_time = float(match.group(1)) if match else -1
                failed = 0
            except subprocess.CalledProcessError:
                avg_time = -1
                failed = 1

            writer.writerow([c, f"{avg_time}ms", r, failed])
```

### Plot des résultats :
Script Python pour générer un barplot avec écart-type (calculé à l'avance) :

```bash
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Lire le CSV
df = pd.read_csv("conc.csv")

# Nettoyer AVG_TIME
df['AVG_TIME'] = df['AVG_TIME'].astype(str).str.replace('ms','').astype(float)

# Calculer la moyenne par param
summary = df.groupby('PARAM')['AVG_TIME'].mean().reset_index()

# Ajouter les écarts-types (calculés à la main)
summary['STD'] = [3.90, 66.77, 82.77, 49.64, 102.78, 0]

# Créer le plot avec Seaborn et ajouter les barres d'erreur
plt.figure(figsize=(8,6))
ax = sns.barplot(x='PARAM', y='AVG_TIME', data=summary, palette='Blues_d')
ax.errorbar(x=range(len(summary)), y=summary['AVG_TIME'], yerr=summary['STD'], fmt='none', c='black', capsize=5)

plt.xlabel('Nombre de requêtes simultanées')
plt.ylabel('Temps moyen par requête (ms)')
plt.title('Benchmark concurrence - TinyInsta')
plt.tight_layout()
plt.savefig("conc.png")
plt.show()
```

![Benchmark](images/conc.png)

---

## **Passage à l'échelle sur taille des données :**

### Post :

Peuplement du Datastore avec 50 utilisateurs, 10,100,1000 posts par utilisateur et 20 followees :

```bash
python seed.py --users 50 --posts 500/5000/50000 --follows-min 20 --follows-max 20
```

Les programmes utilisés sont relativement les mêmes, j'ai tappé les commandes apache à la main puis construis le csv à partir de celles-ci. (Paramètre user différent dans chaque requête)

```bash
ab -n 100 -c 50 -k  https://tp1-massive-data.ew.r.appspot.com/api/timeline?user=user5
```

![Bechmark](images/post.png)

---

### Followee :

Peuplement du Datastore avec 11, 51, 101 utilisateurs 100 posts par utilisateur et 10, 50, 100 followees :

```bash
python3 seed.py --users 11/51/101 --posts 1110/5100/10100 --follows-min 10/50/100 --follows-max 10/50/100
```

Les programmes utilisés sont relativement les mêmes, j'ai tappé les commandes apache à la main puis construis le csv à partir de celles-ci.(Paramètre user différent dans chaque requête)

```bash
ab -n 100 -c 50 -k  https://tp1-massive-data.ew.r.appspot.com/api/timeline?user=user5
```

![Bechmark](images/fanout.png)
