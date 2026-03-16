from datetime import datetime, timedelta
from jose import jwt, JWTError

from app.core.config import get_jwt_algorithm, get_jwt_secret, get_refresh_expire_days, get_access_expire_minutes

ACCESS_TOKEN_EXPIRE_MINUTES = get_access_expire_minutes()
REFRESH_TOKEN_EXPIRE_DAYS = get_refresh_expire_days()
JWT_SECRET = get_jwt_secret()
JWT_ALGORITHM = get_jwt_algorithm()


def create_access_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "type": "access",
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }

    return jwt.encode(
        payload,
        JWT_SECRET,
        algorithm=JWT_ALGORITHM
    )


def create_refresh_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "type": "refresh",
        "exp": datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    }

    return jwt.encode(
        payload,
        JWT_SECRET,
        algorithm=JWT_ALGORITHM
    )


def decode_token(token: str):
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM]
        )

        return payload

    except JWTError:
        return None
