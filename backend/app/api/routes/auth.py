import hashlib
import hmac
import json
import time
import base64

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.responses import SuccessResponse, success_response
from app.core.config import Settings, get_settings
from app.schemas.items import LoginRequest, LoginResponse

router = APIRouter(prefix="/api/auth", tags=["auth"])


def create_token(username: str, secret: str) -> str:
    """Create a simple JWT-like token."""
    header = base64.urlsafe_b64encode(json.dumps({"alg": "HS256", "typ": "JWT"}).encode()).decode().rstrip("=")
    payload_data = {
        "sub": username,
        "iat": int(time.time()),
        "exp": int(time.time()) + 86400 * 7,  # 7 days
    }
    payload = base64.urlsafe_b64encode(json.dumps(payload_data).encode()).decode().rstrip("=")
    signature = hmac.new(secret.encode(), f"{header}.{payload}".encode(), hashlib.sha256).hexdigest()
    return f"{header}.{payload}.{signature}"


def verify_token(token: str, secret: str) -> dict | None:
    """Verify a simple JWT-like token."""
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        header, payload, signature = parts
        expected_sig = hmac.new(secret.encode(), f"{header}.{payload}".encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(signature, expected_sig):
            return None
        # Pad base64
        padding = 4 - len(payload) % 4
        if padding != 4:
            payload += "=" * padding
        payload_data = json.loads(base64.urlsafe_b64decode(payload))
        if payload_data.get("exp", 0) < time.time():
            return None
        return payload_data
    except Exception:
        return None


@router.post("/login")
def login(
    body: LoginRequest,
    settings: Settings = Depends(get_settings),
) -> SuccessResponse[LoginResponse]:
    if body.username != settings.auth_username or body.password != settings.auth_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
        )
    token = create_token(body.username, settings.jwt_secret)
    return success_response(LoginResponse(token=token, username=body.username))


@router.get("/verify")
def verify(
    token: str,
    settings: Settings = Depends(get_settings),
) -> SuccessResponse[dict]:
    payload = verify_token(token, settings.jwt_secret)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
        )
    return success_response({"valid": True, "username": payload.get("sub")})
