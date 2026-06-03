import pandas as pd
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPT_DIR.parent
DATA_DIR = BASE_DIR / "data" / "processed"
SAVED_DIR = BASE_DIR / "data" / "master"
SAVED_DIR.mkdir(parents=True, exist_ok=True)

#Load the cleaned datasets from your directory
df_jiji = pd.read_csv(DATA_DIR / "jiji_cleaned.csv")
df_npc = pd.read_csv(DATA_DIR / "npc_cleaned.csv")
df_ppro = pd.read_csv(DATA_DIR / "ppro_cleaned.csv")

#Add Source column
df_jiji['Source'] = 'Jiji'
df_npc['Source'] = 'NPC'
df_ppro['Source'] = 'PropertyPro'

#Consolidate them together
df_master = pd.concat([df_jiji, df_npc, df_ppro], ignore_index=True)

#Standardize Data Types
df_master['Bedrooms'] = df_master['Bedrooms'].astype('Int64')
df_master['Price (Per Annum)'] = df_master['Price (Per Annum)'].astype('float64')

#Save the consolidated dataset
df_master.to_csv(SAVED_DIR /'abuja_rental_master.csv', index=False)
df_master.head()