from twilio.rest import Client
from Backend.config import settings
import urllib.parse
import os

def send_alert_sms(to_number: str, site_url: str, analysis: str):
    #account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    #auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    #from_number = os.getenv("TWILIO_PHONE_NUMBER")

    #client = Client(account_sid, auth_token)

    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    #Encode site_url for safe query string usage
    encoded_site = urllib.parse.quote(site_url, safe="")
    parent_url_base = "http://127.0.0.1:8000/control"

    from_number = os.getenv("TWILIO_PHONE_NUMBER") or "+0000000000"

    message_body = (
        f"Alert: Your child accessed a suspicious site\n"
        f"AI Analysis: {analysis}\n\n"
        f"Take action: {parent_url_base}?site={encoded_site}"
    )

    client.messages.create(
       body = message_body,
       from_ = from_number,
       to = to_number
    )
