import hashlib
import hmac
import secrets
from datetime import datetime, timezone


def hash_api_key(api_key: str) -> str:
    return hashlib.sha256(api_key.encode("utf-8")).hexdigest()


def generate_api_key() -> str:
    return "ag_" + secrets.token_urlsafe(32)


def verify_hmac_signature(payload: bytes, signature: str, secret: str) -> bool:
    digest = hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(digest, signature)


def timestamp_is_fresh(timestamp: str, max_age_seconds: int) -> bool:
    try:
        ts = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError:
        return False
    now = datetime.now(timezone.utc)
    age = (now - ts).total_seconds()
    return 0 <= age <= max_age_seconds
