import smtplib
from email.mime.text import MIMEText
from app.core.config import settings


def send_email(to_email: str, subject: str, body: str):
    if not settings.SMTP_USERNAME or not settings.SMTP_PASSWORD or not settings.EMAIL_FROM:
        print("EMAIL DEBUG MODE")
        print("TO:", to_email)
        print("SUBJECT:", subject)
        print("BODY:", body)
        return

    message = MIMEText(body)
    message["Subject"] = subject
    message["From"] = settings.EMAIL_FROM
    message["To"] = to_email

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        server.sendmail(settings.EMAIL_FROM, to_email, message.as_string())