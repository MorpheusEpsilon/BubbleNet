from twilio.rest import Client
import os

def send_alert_sms(to_number: str, site_url: str, analysis: str):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_PHONE_NUMBER")

    client = Client(account_sid, auth_token)

    control_link = f"https://yourdomain.com/control?site={site_url}"

    #message_body = (
        #f"Alert: Your child accessed a suspicious site"
        #f"AI Analysis: {analysis}\n\n"
        #f"Take action: {control_link}"
    #)

    #client.messages.create(
        #body=message_body,
        #from_=from_number,
        #to=to_number
    #)
