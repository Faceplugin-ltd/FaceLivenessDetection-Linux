Import `FaceLiveness-API.postman_collection.json`.

baseUrl: `http://127.0.0.1:8084`

Flow: Health → Machine code → Activate (FP1.) → Liveness.

`POST /api/liveness` body: `{ "image": "<base64>" }`

Response `data`: `{ "score": <float>, "result": "Real" | "Spoof", "pass": <bool> }`

Score ≥ 0.5 is Real (`pass: true`). Below 0.5 is Spoof (`pass: false`).
