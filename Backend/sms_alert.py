#Handles the API calls for sendin the SMS text to the parent
from twilio.rest import Client
from Backend.config import settings
import urllib.parse

#Function to send the alert
def send_alert_sms(to_number: str, site_url: str, analysis: str):

    #Possible Errors
    if not settings.TWILIO_ACCOUNT_SID or not settings.TWILIO_AUTH_TOKEN:
        raise RuntimeError("Twilio credentials are missing in environment variables")
    if not settings.TWILIO_PHONE_NUMBER:
        raise RuntimeError("Twilio phone number not configured")

    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    #Encode site_url for safe query
    encoded_site = urllib.parse.quote(site_url, safe="")
    parent_url_base = "http://127.0.0.1:8000/control"

    #Message to send
    message_body = (
        f"Alert: Your child accessed a suspicious site\n"
        f"AI Analysis: {analysis}\n\n"
        f"Take action: {parent_url_base}?site={encoded_site}"
    )

    #Create the message with the body
    client.messages.create(
       body = message_body,
       from_ = settings.TWILIO_PHONE_NUMBER,
       to = to_number
    )
