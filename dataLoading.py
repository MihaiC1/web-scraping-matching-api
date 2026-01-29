from elasticsearch import Elasticsearch, helpers
import pandas as pd

# Conectare simplă (fără securitate)
es = Elasticsearch("http://localhost:9200")

def indexeaza_datele():
    # Citim fișierul unificat creat anterior
    df = pd.read_csv('date_complete_pentru_elasticsearch.csv').fillna("")
    
    # Pregătim datele pentru Elastic
    actions = [
        {
            "_index": "companii",
            "_source": {
                "nume": row['company_commercial_name'],
                "site": row['domain'],
                "telefoane": row['phone_numbers'],
                "social": row['social_links']
            }
        }
        for _, row in df.iterrows()
    ]
    
    # Încărcare masivă (Bulk)
    helpers.bulk(es, actions)
    print(f"Succes! Am încărcat {len(actions)} companii în Elasticsearch.")

if __name__ == "__main__":
    indexeaza_datele()