from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer
from engine.backend.logic.a3_deterministic_engine import A3Engine
from auth.jwt import verify_jwt

app = FastAPI(title="A-3 Engine API")
security = HTTPBearer()
engine = A3Engine()

@app.post("/trade/run")
def run_trade(token=Depends(security)):
    payload = verify_jwt(token.credentials)

    if "trade:run" not in payload["scope"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    engine.run_window(uid=payload["uid"])
    return {"status": "ok"}
