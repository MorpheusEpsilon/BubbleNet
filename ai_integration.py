from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

router = APIRouter()

class LinkRequest(BaseModel):
    url: str

@router.post("/analyze-link")
async def analyze_link(request: LinkRequest):
    try:
        prompt = (
            f"Analyze this link for safety, phishing, malware, adult content, "
            f"or unsafe behavior. Provide a short assessment and a safety score from 0-100:\n{request.url}"
        )

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful security assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        analysis = response.choices[0].message.content.strip()
        return {"url": request.url, "analysis": analysis}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
