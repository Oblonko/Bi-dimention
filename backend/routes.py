"""
Bidimention (A-3) — Backend Route Registry

This module defines and registers all API route groups
exposed by the Bidimention backend.

Responsibilities:
- Centralize route inclusion
- Enforce domain separation
- Keep app.py minimal and authoritative

This file MUST NOT:
- Execute trading logic
- Access exchange APIs
- Mutate engine state
"""

from fastapi import FastAPI

# =========================
# ROUTE IMPORTS
# =========================

# --- Authentication & Identity ---
from backend.routes.auth import router as auth_router

# --- User / Wallet ---
from backend.routes.wallet import router as wallet_router

# --- Ledger & History ---
from backend.routes.ledger import router as ledger_router

# --- Withdrawals ---
from backend.routes.withdraw import router as withdraw_router

# --- Daily / Monthly Summaries ---
from backend.routes.summary import router as summary_router

# --- Audit & Merkle Proofs ---
from backend.routes.audit import router as audit_router

# --- Security / Sessions ---
from backend.routes.security import router as security_router

# --- Admin (read-only / privileged) ---
from backend.routes.admin import router as admin_router

# --- WebSocket Streams ---
from backend.routes.ws import router as ws_router


# =========================
# ROUTE REGISTRATION
# =========================

def register_routes(app: FastAPI) -> None:
    """
    Register all API route groups on the FastAPI app.

    This function is the ONLY place where routes
    should be attached to the application.

    Order matters only for documentation grouping.
    """

    # -------------------------
    # Public / Auth
    # -------------------------
    app.include_router(
        auth_router,
        prefix="/auth",
        tags=["auth"],
    )

    # -------------------------
    # User Wallet & Balance
    # -------------------------
    app.include_router(
        wallet_router,
        prefix="/wallet",
        tags=["wallet"],
    )

    # -------------------------
    # Ledger & Transactions
    # -------------------------
    app.include_router(
        ledger_router,
        prefix="/ledger",
        tags=["ledger"],
    )

    # -------------------------
    # Withdrawals
    # -------------------------
    app.include_router(
        withdraw_router,
        prefix="/withdraw",
        tags=["withdraw"],
    )

    # -------------------------
    # Summaries (Daily / Monthly)
    # -------------------------
    app.include_router(
        summary_router,
        prefix="/summary",
        tags=["summary"],
    )

    # -------------------------
    # Audit / Merkle Proofs
    # -------------------------
    app.include_router(
        audit_router,
        prefix="/audit",
        tags=["audit"],
    )

    # -------------------------
    # Security (Sessions, IPs)
    # -------------------------
    app.include_router(
        security_router,
        prefix="/security",
        tags=["security"],
    )

    # -------------------------
    # Admin (Privileged, Read-Only)
    # -------------------------
    app.include_router(
        admin_router,
        prefix="/admin",
        tags=["admin"],
    )

    # -------------------------
    # WebSocket Streams
    # -------------------------
    app.include_router(
        ws_router,
        prefix="/ws",
        tags=["websocket"],
    )
