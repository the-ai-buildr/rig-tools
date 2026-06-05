"""Password hashing using the standard library (PBKDF2-HMAC-SHA256).

Stored format:  pbkdf2_sha256$<iterations>$<b64 salt>$<b64 hash>
No third-party dependencies required.
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import os

_ALGO = "sha256"
_ITERATIONS = 200_000
_SALT_BYTES = 16


def hash_password(password: str) -> str:
    """Return a salted PBKDF2 hash string for ``password``."""
    salt = os.urandom(_SALT_BYTES)
    derived = hashlib.pbkdf2_hmac(_ALGO, password.encode("utf-8"), salt, _ITERATIONS)
    return "pbkdf2_{algo}${iters}${salt}${hash}".format(
        algo=_ALGO,
        iters=_ITERATIONS,
        salt=base64.b64encode(salt).decode("ascii"),
        hash=base64.b64encode(derived).decode("ascii"),
    )


def verify_password(password: str, stored: str) -> bool:
    """Constant-time verify ``password`` against a stored hash string."""
    try:
        algo_tag, iterations_s, salt_b64, hash_b64 = stored.split("$")
        algo = algo_tag.split("_", 1)[1]
        iterations = int(iterations_s)
        salt = base64.b64decode(salt_b64)
        expected = base64.b64decode(hash_b64)
    except (ValueError, IndexError):
        return False
    derived = hashlib.pbkdf2_hmac(algo, password.encode("utf-8"), salt, iterations)
    return hmac.compare_digest(derived, expected)
