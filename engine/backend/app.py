from __future__ import annotations

import os
import time
from typing import Optional, Dict, Any, List

from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    status,
    Request,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# =========================
# INTERNAL IMPORTS
# =========================

from auth.jwt import (
    decode_jwt,
    issue_jwt,
    JWTPayload,
)

from auth.google_oauth import validate_google_user

from db.firestore import (
    users_repo,
    sessions_repo,
    whitelist_repo,
    login_events_repo,
)

from db.ledger import ledger_repo
from audit.merkle import audit_repo

from core.engine_state import engine_state
from core.scheduler import is_withdraw_open

from logging.cloudwatch import get_logger

# =========================
# CONFIG
# =========================

APP_NAME = "Bidimention A-3 Backend"
ENV = os.getenv("ENV", "production")

ALLOWED_ORIGINS = [
    "https://bidimention.com",
    "https://app.bidimention.com",
    "http://localhost:3000",
]

# =========================
# APP INIT
# =========================

app = FastAPI(
    title=APP_NAME,
    version="1.0.0",
    docs_url="/docs" if ENV != "production" else None,
    redoc_url=None,
)

logger = get_logger("API")

# =========================
# MIDDLEWARE
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# AUTH DEPENDENCY
# =========================

def require_auth(request: Request) -> JWTPayload:
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")

    token = auth.split(" ", 1)[1]
    payload = decode_jwt(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    return payload

# =========================
# GLOBAL ERROR HANDLER
# =========================

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error", extra={"path": request.url.path})
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"},
    )

# =========================
# HEALTH / STATUS
# =========================

@app.get("/health")
def health():
    return {
        "status": "ok",
        "engine": engine_state.status(),
        "time": int(time.time()),
    }

# =========================
# AUTH ROUTES
# =========================

@app.post("/auth/google")
def google_auth(data: Dict[str, Any], request: Request):
    """
    Frontend sends Google ID token.
    Backend:
      - validates Google user
      - checks whitelist
      - issues JWT
      - logs login event
    """
    id_token = data.get("id_token")
    if not id_token:
        raise HTTPException(400, "Missing id_token")

    google_user = validate_google_user(id_token)

    email = google_user.email.lower()
    if not whitelist_repo.is_whitelisted(email):
        raise HTTPException(403, "Email not whitelisted")

    user = users_repo.get_or_create(email=email)

    session = sessions_repo.create(
        uid=user.uid,
        ip=request.client.host,
        user_agent=request.headers.get("user-agent"),
    )

    token = issue_jwt(user.uid, session.session_id)

    login_events_repo.record(
        uid=user.uid,
        email=email,
        ip=request.client.host,
        success=True,
    )

    logger.info("User login", extra={"uid": user.uid})

    return {
        "token": token,
        "uid": user.uid,
    }

# =========================
# USER / WALLET
# =========================

@app.get("/wallet")
def wallet(user=Depends(require_auth)):
    vault = ledger_repo.vault(user.uid)
    return {
        "uid": user.uid,
        "address": vault.deposit_address,
        "balance": vault.balance,
        "min_deposit": 50,
        "withdraw_open": is_withdraw_open(user.uid),
    }

# =========================
# LEDGER
# =========================

@app.get("/ledger")
def ledger(
    limit: int = 50,
    offset: int = 0,
    user=Depends(require_auth),
):
    return ledger_repo.by_uid(
        uid=user.uid,
        limit=limit,
        offset=offset,
    )

# =========================
# WITHDRAW STATUS
# =========================

@app.get("/withdraw/status")
def withdraw_status(user=Depends(require_auth)):
    return {
        "withdraw_open": is_withdraw_open(user.uid),
        "min": 20,
        "max": 2000,
        "fee_pct": 0.03,
    }

# =========================
# DAILY SUMMARY
# =========================

@app.get("/summary/daily")
def daily_summary(user=Depends(require_auth)):
    return ledger_repo.daily_summary(user.uid)

# =========================
# AUDIT
# =========================

@app.get("/audit/root/daily")
def audit_root_daily(user=Depends(require_auth)):
    return {
        "root": audit_repo.current_root(),
    }

# =========================
# WEBSOCKET — GLYPHS
# =========================

@app.websocket("/ws/glyphs")
async def glyph_stream(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            glyph = engine_state.next_glyph()
            if glyph:
                await ws.send_json(glyph)
            await ws.receive_text()  # keepalive
    except WebSocketDisconnect:
        logger.info("Glyph WS disconnected")

# =========================
# SHUTDOWN
# =========================

@app.on_event("shutdown")
def on_shutdown():
    logger.info("API shutting down")
