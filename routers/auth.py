import os

from fastapi import APIRouter, HTTPException

from dotenv import load_dotenv

from utils.auth import create_token

load_dotenv()

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/login")
def login(data: dict):

    email = data.get("email")
    password = data.get("password")

    admin_email = os.getenv("ADMIN_EMAIL")
    admin_password = os.getenv("ADMIN_PASSWORD")

    if email != admin_email or password != admin_password:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_token(email)

    return {
        "success": True,
        "token": token
    }