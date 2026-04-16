import os
import smtplib
from email.mime.text import MIMEText

from dotenv import load_dotenv

load_dotenv()


class MailSender:
    def __init__(self):
        self.sender = os.environ["EMAIL_SENDER"]
        self.password = os.environ["EMAIL_PASSWORD"]
        self.recipient = os.environ["EMAIL_RECIPIENT"]

    def send_email(self, subject: str, body: str):
        msg = MIMEText(body, "html")
        msg["Subject"] = subject
        msg["From"] = self.sender
        msg["To"] = self.recipient

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(self.sender, self.password)
            server.send_message(msg)


__all__ = ["MailSender"]
