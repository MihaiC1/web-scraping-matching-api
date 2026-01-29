import pandas as pd

# 1. Încărcăm datele
# df_nume conține: website, company_name
df_nume = pd.read_csv('sample-websites-company-names.csv')

# df_date conține: website, phone_numbers, social_links, status
df_date = pd.read_csv('rezultate_scraping.csv')

# 2. Curățăm coloana 'website' pentru a asigura o potrivire perfectă
# Eliminăm spațiile libere și forțăm litere mici
df_nume['domain'] = df_nume['domain'].str.strip().str.lower()
df_date['domain'] = df_date['domain'].str.strip().str.lower()

# 3. Executăm unificarea (Merge)
# 'left' înseamnă că păstrăm toate companiile din lista originală, 
# chiar dacă pentru unele nu am găsit date la scraping.
df_final = pd.merge(df_nume, df_date, on='domain', how='left')

# 4. Curățăm rezultatul final
# Înlocuim valorile goale (NaN) cu un string gol pentru a arăta mai bine în baza de date
df_final = df_final.fillna('')

# 5. Salvăm fișierul final
df_final.to_csv('date_complete_pentru_elasticsearch.csv', index=False)

print("--- Proces finalizat ---")
print(f"Total companii procesate: {len(df_final)}")
print(f"Exemplu date unificate:\n", df_final.head(3))