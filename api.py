from fastapi import FastAPI, Query
from elasticsearch import Elasticsearch

app = FastAPI()
es = Elasticsearch("http://localhost:9200")

@app.get("/match-company")
async def match_company(
    name: str = Query(None),
    phone: str = Query(None),
    website: str = Query(None)
):
    # Construim o căutare inteligentă
    # "should" înseamnă că încercăm să potrivim oricare dintre câmpuri
    # "^3" înseamnă că numele are prioritate (pondere) mai mare
    must_match = []
    if name: must_match.append({"match": {"nume": {"query": name, "fuzziness": "AUTO"}}})
    if phone: must_match.append({"match": {"telefoane": phone}})
    if website: must_match.append({"match": {"site": website}})

    query = {
        "query": {
            "bool": {
                "should": must_match
            }
        }
    }

    res = es.search(index="companii", body=query, size=1)
    
    if res['hits']['hits']:
        return {
            "match_found": True,
            "data": res['hits']['hits'][0]['_source'],
            "score": res['hits']['hits'][0]['_score']
        }
    
    return {"match_found": False, "message": "Nu am găsit nicio potrivire."}

# Pentru a rula API-ul, scrie în terminal: 
# py -m uvicorn api:app --reload