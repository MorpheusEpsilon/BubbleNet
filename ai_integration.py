from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
from openai import OpenAI
from dotenv import load_dotenv
from sms_alert import send_alert_sms  # ✅ Import SMS trigger
import re

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
router = APIRouter()

class LinkRequest(BaseModel):
    url: str

@router.post("/analyze-link")
async def analyze_link(request: LinkRequest):
    try:
        # Adult prompt (detailed + numeric score)
        adult_prompt = (
            f"Analyze this link for safety, phishing, malware, adult content, and unsafe behavior. "
            f"Provide a short assessment in less than 50 words AND a numeric safety score from 0-100. "
            f"Format it like this:\n"
            f"Assessment: <your text>\nSafety Score: <number>\n{request.url}"
        )

        # Kid-friendly prompt (simple, fun, easy to understand)
        kid_prompt = (
            f"Explain whether this link is safe or risky for a 5-15 year old in an easy way. "
            f"In less than 50 words, explain why it's dangerous or safe. Make it playful:\n{request.url}"
        )

        # Adult analysis + score in one call
        adult_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful security assistant."},
                {"role": "user", "content": adult_prompt}
            ],
            temperature=0
        )
        adult_analysis = adult_response.choices[0].message.content.strip()

        # Extract numeric score from adult analysis
        match = re.search(r"Safety Score[:\s]*([0-9]{1,3})", adult_analysis)
        security_rating = int(match.group(1)) if match else 0

        # Boolean unsafe: check keywords AND override if score <=50
        unsafe = any(
            word in adult_analysis.lower()
            for word in ["phishing", "malware", "unsafe", "danger", "risky", "adult content"]
        ) and security_rating > 50

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

        # ✅ Trigger SMS alert to parent
        send_alert_sms(
            to_number="+525584922217",  # Replace with actual parent number
            site_url=request.url,
            analysis=adult_analysis
        )

        return {
            "url": request.url,
            "adult_analysis": adult_analysis,
            "kid_analysis": kid_analysis,
            "unsafe": unsafe,
            "safety_score": security_rating  # Numeric score consistent with adult analysis
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
