from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
from openai import OpenAI
from dotenv import load_dotenv
from Backend.config import settings
from Backend.sms_alert import send_alert_sms
from . import storage
import re

load_dotenv()
router = APIRouter()
client = OpenAI(api_key=settings.OPENAI_API_KEY)


class LinkRequest(BaseModel):
    url: str

@router.post("/analyze-link")                   #Ruta para IA
async def analyze_link(request: LinkRequest):
    site_url = request.url.lower()
    #----Primer Acto:
    if site_url in storage.get_whitelist():
        return {
            "url": site_url,
            "adult_analysis": "Site is whitelisted ✅",
            "kid_analysis": "Safe for kids ✅",
            "unsafe": False,
            "safety_score": 100
        }
    elif site_url in storage.get_blacklist():
        # Auto-send SMS alert
        to_number = os.getenv("PARENT_PHONE") or "+00000"
        send_alert_sms(
        to_number,  # Or settings.PARENT_PHONE
        site_url = site_url,
        analysis="Site is blacklisted ⛔"
        )
        return {
            "url": site_url,
            "adult_analysis": "Site is blacklisted ⛔",
            "kid_analysis": "Not safe for kids ⛔",
            "unsafe": True,
            "safety_score": 0
        }


    #----Segundo Acto:
    try:
        # Adult prompt
        adult_prompt = (
            f"Analyze this link for safety, phishing, malware, adult content, give warnings if they're messaging or social media. In less than 50 words, "
            f"or unsafe behavior. Provide a short assessment and a safety score from 0-100:\n{request.url}"
        )

        # Kid-friendly prompt
        kid_prompt = (
            f"Explain whether this link is safe or risky for a 5-15 year old in an easy way. In less than 50 words, but explain why it's dangerous or safe, "
            f"Use very simple words and make it playful:\n{request.url}"
        )

        # Adult analysis
        adult_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful security assistant."},
                {"role": "user", "content": adult_prompt}
            ],
            temperature=0
        )
        adult_analysis = adult_response.choices[0].message.content.strip()

        # Kid-friendly analysis
        kid_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for kids, playful and simple."},
                {"role": "user", "content": kid_prompt}
            ],
            temperature=0.7
        )
        kid_analysis = kid_response.choices[0].message.content.strip()


        #----Tercer acto:

        # Trigger SMS alert to parent
        #send_alert_sms(
        #    to_number="+525584922217",  # Replace with actual parent number
        #    site_url=request.url,
        #    analysis=adult_analysis
        #)
        #send_alert_sms(settings.PARENT_PHONE, request.url, adult_analysis)

        # Extract safety score, first number found.
        score_match = re.search(r"\b(\d{1,3})\b", adult_analysis)
        safety_score = int(score_match.group(1)) if score_match else None

        # Boolean logic: unsafe if score < 50
        unsafe = safety_score is not None and safety_score < 50

        if unsafe:
            to_number = os.getenv("PARENT_PHONE") or "+0000000000"
            send_alert_sms(
                to_number,
                site_url = site_url,
                analysis = adult_analysis
            )

        return {
            "url": request.url,
            "adult_analysis": adult_analysis,
            "kid_analysis": kid_analysis,
            "unsafe": unsafe,  # <-- extension expects this
            "safety_score": safety_score or 100
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
