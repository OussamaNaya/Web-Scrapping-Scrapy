import pandas as pd

# Charger le fichier JSON
df = pd.read_json('output.json')

# Sauvegarder le fichier en format CSV
df.to_csv('data.csv', index=False)
