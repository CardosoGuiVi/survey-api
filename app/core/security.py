import hashlib
import hmac
from datetime import UTC, datetime, timedelta
from typing import Any, TypedDict

import bcrypt
import jwt

from app.core.config import settings


# Senha
def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())


# JWT
class TokenRequest(TypedDict, total=False):
    user_id: str
    workspace_id: str
    role: str
    exp: datetime


def create_access_token(payload: dict[str, Any]) -> str:
    data = payload.copy()
    expire = datetime.now(UTC) + timedelta(minutes=settings.jwt_expire_minutes)
    data["exp"] = expire
    return jwt.encode(data, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict[str, Any]:
    return jwt.decode(
        token,
        settings.jwt_secret,
        algorithms=[settings.jwt_algorithm],
    )


# ──────────────────────────────────────────────
# Anonimização — irreversível por design
#
# O token identifica a pessoa apenas para evitar
# resposta dupla. Nunca pode ser revertido para
# descobrir quem é o usuário — nem pelo Admin,
# nem pelo banco.
#
# Propriedades garantidas por teste:
#   - mesmo user + mesmo workspace → mesmo token (detecta duplicata)
#   - mesmo user + workspace diferente → token diferente (isolamento)
#   - token não contém user_id (irreversível)
# ──────────────────────────────────────────────


def generate_anon_token(user_id: str, workspace_salt: str) -> str:
    """
    Gera token anônimo irreversível.
    Usa HMAC-SHA256 com o salt do workspace como chave.
    """
    return hmac.new(
        workspace_salt.encode(),
        user_id.encode(),
        hashlib.sha256,
    ).hexdigest()
