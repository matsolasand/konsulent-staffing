from fastapi import FastAPI, Query
import requests
import json

def hent_konsulentregister():
    response = requests.get("http://server:8000/konsulenter")
    data = response.json()
    return data

# ------------------------------------------------------------------

def filtrer_konsulenter(
    konsulenter : list[dict],
    min_tilgjengelighet_prosent : int,
    pakrevde_ferdigheter : list[str]
) -> list[dict]:
    tilgjengelige_konsulenter = []
    for konsulent in konsulenter:
        tilgjengelighet = 100 - konsulent["belastning_prosent"]
        har_ferdigheter = all(
            ferdighet in konsulent["ferdigheter"]
            for ferdighet in pakrevde_ferdigheter
        )
        if har_ferdigheter and tilgjengelighet >= min_tilgjengelighet_prosent:
            tilgjengelige_konsulenter.append({
                "navn" : konsulent["navn"],
                "tilgjengelighet" : tilgjengelighet
            })
    return tilgjengelige_konsulenter

# ------------------------------------------------------------------

def lag_sammendrag(
    tilgjengelige_konsulenter : list[dict],
    min_tilgjengelige_prosent : int,
    pakrevde_ferdigheter : list[str]
) -> list[dict]:
    sammendrag = []
    strengkonvensjon(
        sammendrag,
        tilgjengelige_konsulenter,
        min_tilgjengelige_prosent,
        pakrevde_ferdigheter
    )
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
    respons["sammendrag"] = respons["sammendrag"].replace(" .", ".")
    return respons

# ------------------------------------------------------------------

def strengkonvensjon(
    sammendrag : list[str],
    tilgjengelige_konsulenter : list[dict],
    min_tilgjengelige_prosent : int,
    pakrevde_ferdigheter : list[str]
) -> None:
    if len(tilgjengelige_konsulenter) == 1:
        sammendrag.append(
            f"Fant {len(tilgjengelige_konsulenter)} konsulent med minst"
        )
    else:
        sammendrag.append(
            f"Fant {len(tilgjengelige_konsulenter)} konsulenter med minst"
        )
    if len(pakrevde_ferdigheter) == 1:
        sammendrag.append(
            f"{min_tilgjengelige_prosent}% tilgjengelighet og ferdigheten "
            + f"'{pakrevde_ferdigheter[0]}'."
        )
        return
    sammendrag.append(
        f"{min_tilgjengelige_prosent}% tilgjengelighet og ferdighetene"
    )
    for i in range(len(pakrevde_ferdigheter)):
        sammendrag.append(f"'{pakrevde_ferdigheter[i]}'")
        if (i + 1) < len(pakrevde_ferdigheter):
            sammendrag.append("og")
    sammendrag.append(".")

# ------------------------------------------------------------------

app = FastAPI()

@app.get("/tilgjengelige-konsulenter/sammendrag")
def sammendrag_egnede_konsulenter(
    min_tilgjengelighet_prosent : int = Query(..., ge=50, le=100),
    pakrevde_ferdigheter : list[str] = Query(...)
):
    konsulentregister = hent_konsulentregister()
    tilgjengelige_konsulenter = filtrer_konsulenter(
        konsulenter = konsulentregister,
        min_tilgjengelighet_prosent = min_tilgjengelighet_prosent,
        pakrevde_ferdigheter = pakrevde_ferdigheter
    )
    respons = lag_sammendrag(
        tilgjengelige_konsulenter = tilgjengelige_konsulenter,
        min_tilgjengelige_prosent = min_tilgjengelighet_prosent,
        pakrevde_ferdigheter = pakrevde_ferdigheter
    )
    return respons


def main():
    respons = sammendrag_egnede_konsulenter(
        min_tilgjengelighet_prosent = 50,
        pakrevde_ferdigheter = ["python", "c++"]
    )
    print(respons)

if __name__ == "__main__":
    main()