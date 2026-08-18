from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import aiosmtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")


class ContactForm(BaseModel):
    name: str
    phone: str
    email: str
    subject: str
    message: str


@router.post("/contact")
async def contact(form: ContactForm):

    # Check environment variables
    if not EMAIL_USER:
        raise HTTPException(
            status_code=500,
            detail="EMAIL_USER is missing"
        )

    if not EMAIL_PASSWORD:
        raise HTTPException(
            status_code=500,
            detail="EMAIL_PASSWORD is missing"
        )

    if not RECEIVER_EMAIL:
        raise HTTPException(
            status_code=500,
            detail="RECEIVER_EMAIL is missing"
        )

    msg = EmailMessage()

    msg["Subject"] = f"New Contact Form - {form.subject}"
    msg["From"] = EMAIL_USER
    msg["To"] = RECEIVER_EMAIL
    msg["Reply-To"] = form.email

    msg.set_content(
        f"""
New Contact Form
================

Name: {form.name}
Phone: {form.phone}
Email: {form.email}

Subject:
{form.subject}

Message:
{form.message}
"""
    )

    try:

        await aiosmtplib.send(
            msg,
            hostname="smtp.gmail.com",
            port=587,
            start_tls=True,
            username=EMAIL_USER,
            password=EMAIL_PASSWORD,
        )

        print("EMAIL SENT SUCCESSFULLY")

        return {
            "success": True,
            "message": "Email sent successfully"
        }

    except Exception as e:

        print("================================")
        print("EMAIL ERROR:", repr(e))
        print("================================")

        raise HTTPException(
            status_code=500,
            detail=f"Email sending failed: {str(e)}"
        )
