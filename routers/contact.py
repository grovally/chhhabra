from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import aiosmtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

# .env se values read hongi
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

    if not EMAIL_USER or not EMAIL_PASSWORD or not RECEIVER_EMAIL:
        raise HTTPException(
            status_code=500,
            detail="Email configuration is missing"
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

        return {
            "success": True,
            "message": "Email sent successfully"
        }

    except Exception as e:
        print("EMAIL ERROR:", str(e))

        raise HTTPException(
            status_code=500,
            detail="Failed to send email"
        )
