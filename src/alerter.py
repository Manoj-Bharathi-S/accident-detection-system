import mailtrap as mt
from src.config import RECEIVER_EMAIL, MAILTRAP_TOKEN, SENDER_EMAIL

def send_alert_email(severity, cause, coordinates):
    if not MAILTRAP_TOKEN:
        print(f"[ALERT WARNING] Email not sent due to missing MAILTRAP_TOKEN. (Severity: {severity}, Cause: {cause})")
        return False
        
    subject = f"EMERGENCY: {severity} Road Accident Detected"
    body = f"""
    A road accident has been detected by the AI Monitor.
    
    Severity: {severity}
    Estimated Cause: {cause}
    Location: {coordinates}
    Google Maps Link: https://www.google.com/maps/search/?api=1&query={coordinates[0]},{coordinates[1]}
    
    Please dispatch emergency services immediately.
    """
    
    mail = mt.Mail(
        sender=mt.Address(email=SENDER_EMAIL, name="AI Accident Monitor"),
        to=[mt.Address(email=RECEIVER_EMAIL)],
        subject=subject,
        text=body,
        category="Emergency Alert",
    )
    
    try:
        client = mt.MailtrapClient(token=MAILTRAP_TOKEN)
        response = client.send(mail)
        print("[ALERT] Emergency email sent via Mailtrap successfully.")
        return True
    except Exception as e:
        print(f"[ALERT ERROR] Failed to send email via Mailtrap: {e}")
        return False
