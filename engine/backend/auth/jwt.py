from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any

from jose import JWTError, jwt
from fastapi import HTTPException, status
import os

# ======================================================
# ENV
# ======================================================

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "CHANGE_ME")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_ISSUER = os.getenv("JWT_ISSUER", "bidimention")
JWT_AUDIENCE = os.getenv("JWT_AUDIENCE", "bidimention-api")

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15")
)
REFRESH_TOKEN_EXPIRE_DAYS = int(
    os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "30")
)

# ======================================================
# TOKEN CREATION
# ======================================================

def _create_token(
    *,
    subject: str,
    token_type: str,
    expires_delta: timedelta,
    extra_claims: Optional[Dict[str, Any]] = None,
) -> str:
    now = datetime.now(timezone.utc)

    payload = {
        "sub": subject,
        "typ": token_type,
        "iat": int(now.timestamp()),
        "nbf": int(now.timestamp()),
        "exp": int((now + expires_delta).timestamp()),
        "iss": JWT_ISSUER,
        "aud": JWT_AUDIENCE,
    }

    if extra_claims:
        payload.update(extra_claims)

    return jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )


def create_access_token(
    *,
    user_id: str,
    is_admin: bool = False,
    scopes: Optional[list[str]] = None,
) -> str:
    return _create_token(
        subject=user_id,
        token_type="access",
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        extra_claims={
            "admin": is_admin,
            "scopes": scopes or [],
        },
    )


def create_refresh_token(*, user_id: str) -> str:
    return _create_token(
        subject=user_id,
        token_type="refresh",
        expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
    )

# ======================================================
# TOKEN VERIFICATION
# ======================================================

def decode_token(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
            audience=JWT_AUDIENCE,
            issuer=JWT_ISSUER,
        )
        return payload

    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e


def verify_access_token(token: str) -> Dict[str, Any]:
    payload = decode_token(token)

    if payload.get("typ") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
        )

    return payload


def verify_refresh_token(token: str) -> Dict[str, Any]:
    payload = decode_token(token)

    if payload.get("typ") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    return payload

# ======================================================
# ROLE / PERMISSION HELPERS
# ======================================================

def require_admin(payload: Dict[str, Any]) -> None:
    if not payload.get("admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )


def require_scope(payload: Dict[str, Any], scope: str) -> None:
    scopes = payload.get("scopes", [])
    if scope not in scopes:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Missing required scope: {scope}",
)
