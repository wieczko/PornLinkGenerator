import hashlib
import hmac
import json
import os
from datetime import datetime, timedelta

SERIAL_PREFIX = "PLG"
SERIAL_VERSION = "V1"
SECRET_KEY = "PornLinkGenerator-2026-Licence-Key-7F3C9A13"
LICENSE_DIR = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "PornLinkGenerator")
LICENSE_FILE = os.path.join(LICENSE_DIR, "license.json")


def _normalize_username(username: str) -> str:
    name = (username or "").strip()
    if not name:
        raise ValueError("Nazwa użytkownika nie może być pusta.")
    return " ".join(name.split())


def _username_token(username: str) -> str:
    normalized = _normalize_username(username).lower()
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:10].upper()


def _payload(username: str, expiry: str) -> str:
    return f"{SERIAL_VERSION}|{_username_token(username)}|{expiry}"


def _signature(payload: str) -> str:
    return hmac.new(SECRET_KEY.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256).hexdigest()[:12].upper()


def generate_license(username: str = "default-user", days: int = 3650) -> str:
    username = _normalize_username(username)
    if days <= 0:
        raise ValueError("Dni licencji muszą być większe od zera.")

    expiry_date = (datetime.utcnow() + timedelta(days=days)).strftime("%Y%m%d")
    payload = _payload(username, expiry_date)
    signature = _signature(payload)
    return f"{SERIAL_PREFIX}-{_username_token(username)}-{expiry_date}-{signature}"


def validate_license(serial: str, username: str = "") -> bool:
    try:
        cleaned = (serial or "").strip().upper()
        if not cleaned or not cleaned.startswith(f"{SERIAL_PREFIX}-"):
            return False

        parts = cleaned.split("-")
        if len(parts) != 4:
            return False

        prefix, user_token, expiry, signature = parts
        if prefix != SERIAL_PREFIX:
            return False
        if len(user_token) != 10 or len(signature) != 12:
            return False

        payload = f"{SERIAL_VERSION}|{user_token}|{expiry}"
        if not hmac.compare_digest(signature, _signature(payload)):
            return False

        try:
            expiry_date = datetime.strptime(expiry, "%Y%m%d").date()
        except ValueError:
            return False

        return datetime.utcnow().date() <= expiry_date
    except Exception:
        return False


def load_license() -> dict:
    try:
        if not os.path.exists(LICENSE_FILE):
            return {}
        with open(LICENSE_FILE, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        if isinstance(data, dict):
            return data
    except Exception:
        pass
    return {}


def save_license(username: str, serial: str) -> None:
    os.makedirs(LICENSE_DIR, exist_ok=True)
    with open(LICENSE_FILE, "w", encoding="utf-8") as handle:
        json.dump({"username": _normalize_username(username), "serial": serial.strip().upper()}, handle, ensure_ascii=False)


def remove_license() -> None:
    try:
        if os.path.exists(LICENSE_FILE):
            os.remove(LICENSE_FILE)
    except Exception:
        pass
