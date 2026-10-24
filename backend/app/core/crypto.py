import base64
import hashlib
import os

from cryptography.fernet import Fernet

from app.core.config import get_settings

_DEV_KEY = base64.urlsafe_b64encode(
    hashlib.sha256(b"02-bias-detector-dev-only-key").digest()
).decode()

_fernet: Fernet | None = None


def get_fernet() -> Fernet:
    global _fernet
    if _fernet is None:
        key = os.getenv("FERNET_KEY") or get_settings().fernet_key or _DEV_KEY
        _fernet = Fernet(key.encode() if isinstance(key, str) else key)
    return _fernet


def encrypt_text(plain: str) -> str:
    return get_fernet().encrypt(plain.encode()).decode()


def decrypt_text(token: str) -> str:
    return get_fernet().decrypt(token.encode()).decode()
