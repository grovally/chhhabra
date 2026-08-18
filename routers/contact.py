from fastapi import APIRouter
from pydantic import BaseModel
import os
import aiosmtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

EMAIL_USER = os.getenv("chhabrapropertiesofficial@gmail.com")
EMAIL_PASSWORD = os.getenv("jcwljlqppfaxswzy")
RECEIVER_EMAIL = os.getenv("chhabrapropertiesofficial@gmail.com")


class ContactForm(BaseModel):
    name: str
    phone: str
    email: str
    subject: str
    message: str


@router.post("/contact")
async def contact(form: ContactForm):
    msg = EmailMessage()

    msg["Subject"] = f"New Contact Form - {form.subject}"
    msg["From"] = EMAIL_USER
    msg["To"] = RECEIVER_EMAIL

    msg.set_content(f"""
New Contact Form

Name: {form.name}
Phone: {form.phone}
Email: {form.email}

Subject:
{form.subject}

Message:
{form.message}
""")

    await aiosmtplib.send(
        msg,
        hostname="smtp.gmail.com",
        port=587,
        start_tls=True,
        username=EMAIL_USER,
        password=EMAIL_PASSWORD,
    )

    return {"message": "Email sent successfully"}
