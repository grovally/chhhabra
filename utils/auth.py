import os

from datetime import datetime, timedelta, timezone

from jose import jwt, JWTError
from fastapi import Header, HTTPException

from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"


def create_token(email: str):

    expire = datetime.now(timezone.utc) + timedelta(hours=24)

    payload = {
        "sub": email,
        "exp": expire
    }

    return jwt.encode(
        payload,
        JWT_SECRET,
        algorithm=ALGORITHM
    )


def verify_token(authorization: str = Header(None)):

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization token missing"
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization"
        )

    token = authorization.split(" ")[1]

    try:

        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")

        if not email:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return email

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Token expired or invalid"
        )