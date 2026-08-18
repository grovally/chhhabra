from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import resend
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

# Resend API Key
resend.api_key = os.getenv("RESEND_API_KEY")


class ContactForm(BaseModel):
    name: str
    phone: str
    email: str
    subject: str
    message: str


@router.post("/contact")
async def contact(form: ContactForm):

    if not resend.api_key:
        raise HTTPException(
            status_code=500,
            detail="RESEND_API_KEY is missing"
        )

    try:

        response = resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": "chhabrapropertiesofficial@gmail.com",
            "reply_to": form.email,
            "subject": f"New Contact Form - {form.subject}",
            "html": f"""
                <h2>New Contact Form</h2>

                <p><strong>Name:</strong> {form.name}</p>

                <p><strong>Phone:</strong> {form.phone}</p>

                <p><strong>Email:</strong> {form.email}</p>

                <p><strong>Subject:</strong> {form.subject}</p>

                <h3>Message</h3>

                <p>{form.message}</p>
            """
        })

        print("RESEND RESPONSE:", response)

        return {
            "success": True,
            "message": "Email sent successfully"
        }

    except Exception as e:

        print("RESEND ERROR:", repr(e))

        raise HTTPException(
            status_code=500,
            detail=f"Email sending failed: {str(e)}"
        )
