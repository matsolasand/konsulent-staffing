from fastapi import FastAPI
import json

app = FastAPI()

json_filsti = "konsulenter.json"

@app.get("/konsulenter")
def hent_konsulenter():
    try:
        with open(json_filsti) as konsulentfil:
            konsulenter = json.load(konsulentfil)
        return konsulenter
    except FileNotFoundError:
        return {"error": f"Ingen fil med filnavn {json_filsti}."}
    except json.JSONDecodeError:
        return {"error": "Klarte ikke å dekode JSON fra fil."}