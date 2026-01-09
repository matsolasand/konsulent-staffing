from fastapi import FastAPI, Query
import requests
import json

def hent_konsulentregister():
    response = requests.get("http://localhost:8000/konsulenter")
    data = response.json()
    return data

# ----------------------------------------------------------------------

def filtrer_konsulenter(
    konsulenter : list[dict],
    min_tilgjengelighet_prosent : int,
    påkrevd_ferdighet : str
) -> list[dict]:
    tilgjengelige_konsulenter = []
    for konsulent in konsulenter:
        ferdigheter = konsulent["ferdigheter"]
        tilgjengelighet = 100 - konsulent["belastning_prosent"]
        if (
            påkrevd_ferdighet in ferdigheter
        ) and (
            tilgjengelighet >= min_tilgjengelighet_prosent
        ):
            tilgjengelig = {
                "navn" : konsulent["navn"],
                "tilgjengelighet" : tilgjengelighet
            }
            tilgjengelige_konsulenter.append(tilgjengelig)
    return tilgjengelige_konsulenter

# ----------------------------------------------------------------------

def lag_sammendrag(
    tilgjengelige_konsulenter : list[dict],
    min_tilgjengelige_prosent : int,
    påkrevd_ferdighet : str
) -> list[dict]:
    sammendrag = [
        f"Fant {len(tilgjengelige_konsulenter)} konsulenter med minst "
        + f"{min_tilgjengelige_prosent}% tilgjengelighet og ferdigheten "
        + f"{påkrevd_ferdighet}."
    ]
    for konsulent in tilgjengelige_konsulenter:
        navn = konsulent["navn"]
        tilgjengelighet = konsulent["tilgjengelighet"]
        sammendrag.append(
            f"{navn}. har {tilgjengelighet}% "
            + "tilgjengelighet."
        )
    respons = {
        "sammendrag" : " ".join(sammendrag)
    }
    return respons

# ----------------------------------------------------------------------

app = FastAPI()

@app.get("/tilgjengelige-konsulenter/sammendrag")
def sammendrag_egnede_konsulenter(
    min_tilgjengelighet_prosent : int = Query(..., ge=50, le=100),
    påkrevd_ferdighet : str = Query(...)
):
    konsulentregister = hent_konsulentregister()
    tilgjengelige_konsulenter = filtrer_konsulenter(
        konsulenter = konsulentregister,
        min_tilgjengelighet_prosent = min_tilgjengelighet_prosent,
        påkrevd_ferdighet = påkrevd_ferdighet
    )
    respons = lag_sammendrag(
        tilgjengelige_konsulenter = tilgjengelige_konsulenter,
        min_tilgjengelige_prosent = min_tilgjengelighet_prosent,
        påkrevd_ferdighet = påkrevd_ferdighet
    )
    respons = json.dumps(respons)
    return respons


def main():
    respons = sammendrag_egnede_konsulenter(
        min_tilgjengelighet_prosent = 50, påkrevd_ferdighet = "python"
    )
    print(respons)

if __name__ == "__main__":
    main()