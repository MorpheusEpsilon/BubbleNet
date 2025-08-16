from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

router = APIRouter()

class LinkRequest(BaseModel):
    url: str

@router.post("/analyze-link")
async def analyze_link(request: LinkRequest):
    try:
        # Adult prompt (detailed)
        adult_prompt = (
            f"Analyze this link for safety, phishing, malware, adult content, "
            f"or unsafe behavior. Provide a short assessment and a safety score from 0-100:\n{request.url}"
        )

        # Kid-friendly prompt (simple, fun, easy to understand)
        kid_prompt = (
            f"Explain whether this link is safe or risky for a kid in a fun and easy way. "
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
            temperature=0.7  # a bit more creative for fun phrasing
        )
        kid_analysis = kid_response.choices[0].message.content.strip()

        return {
            "url": request.url,
            "adult_analysis": adult_analysis,
            "kid_analysis": kid_analysis
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
