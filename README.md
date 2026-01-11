# Konsulent-staffing (case-intervju)
En MCP-basert løsning for en intern AI-assistent, bygget med Python/FastAPI.
AI-assistenten kaller på løsningen for å finne konsulenter med én eller flere
aktuelle ferdigheter og som er mer enn en gitt prosent tilgjengelige.

## Forutsetninger
- Docker og Docker Compose

## Hurtigstart
Start Docker Desktop
docker compose up --build

## Arkitektur
rotkatalogen inneholder mappene
* server/
* klient/
* testing/
samt filene
* README.md
* .gitignore
* compose.yaml
* the_case.txt

### server
* JSON-fil med tilgjengelige konsulenter og deres ferdigheter samt tilgjengelighet i prosent. * main.py som henter og returnerer JSON-fila med alle konsulentene.
* Dockerfile

### klient
* main.py. Her ligger tjenesten som AI-assistenten kaller på. Tjenesten henter registeret med konsulenter, filtrerer tilgjenglige konsulenter og returnerer et leselig sammendrag.
* Dockerfile

### testing
* test_openrouter.py som kan teste gjennomføringsevnen til fire forskjellige modeller. Den kan gjøre det med muligheten for flere ferdigheter (standard).
* modelltesting.txt som inneholder en kortere analyse av testingen gjort for de fire modellene man kan teste i test_openrouter.py. Det er blitt gjort analyse for både versjonen som kun tok inn én ferdighet som en stren og for versjonen som tar flere ferdigheter som en liste med strenger.

#### README.md
Dette er README, du leser den allerede!

#### .gitignore
Denne har vært i bruk tidligere, men er tom for øyeblikket.

#### compose.yaml
Denne er for "docker compose up".

#### the_case.txt
Dette er caseteksten/oppgaven for dette repositoriet.

## Testing av API-et

Test server direkte:
```bash
curl http://localhost:8000/konsulenter
```

Test klient med én ferdighet:
```bash
curl -G "http://localhost:8001/tilgjengelige-konsulenter/sammendrag" \
  --data-urlencode "min_tilgjengelighet_prosent=50" \
  --data-urlencode "pakrevde_ferdigheter=python"
```

Test klient med flere ferdigheter:
```bash
curl -G "http://localhost:8001/tilgjengelige-konsulenter/sammendrag" \
  --data-urlencode "min_tilgjengelighet_prosent=50" \
  --data-urlencode "pakrevde_ferdigheter=python" \
  --data-urlencode "pakrevde_ferdigheter=c++"
```

## LLM-integrasjonstesting
Vi kan teste forskjellige LLM-modeller på verktøyet vårt med test_openrouter.py. Dette scriptet tester for modellene
* Claude 3.5 Haiku
* GPT-4o-mini
* GPT-3.5-turbo
* Llama 3.1 8B
Parametrene som kan endres på ligger under kommentaren "parameters" i funksjonen main(). Her kan man velge hvilken modell man vil teste, og man vil se responsen fra modellen hos OpenRouter eller se om modellen klarte oppgaven. Programmet kjøres etter at "docker compose up".
1. Sett OPENROUTER_API_KEY i test_openrouter.py (øverst i scriptet)
2. Kjør: python testing/test_openrouter.py
3. Se modelltesting.txt for analyse

## Prosjektstruktur
project-root/
│
├── server/
│   ├── main.py
|   ├── konsulenter.json
│   └── Dockerfile
│
├── klient/
│   ├── main.py
│   └── Dockerfile
│
├── testing/
│   ├── test_openrouter.py
│   └── modelltesting.txt
│
├── README.md
├── .gitignore
├── compose.yaml
└── the_case.txt