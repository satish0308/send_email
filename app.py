import os
import smtplib
from email.message import EmailMessage
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from socket import timeout
import yaml
from dotenv import load_dotenv

load_dotenv()

with open("config.yaml", "r") as f:
    data = yaml.safe_load(f)

EMAIL_FROM = data["FROM_EMAIL"]
EMAILS_TO = data["TO_EMAIL"]

URL_TO_CHECK = "https://s3.minikubesgh.dpdns.org/"
TIMEOUT_SECONDS = 10

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587

SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")



def check_url(url: str, timeout_seconds: int = 10) -> bool:
    try:
        with urlopen(url, timeout=timeout_seconds) as response:
            return 200 <= response.status < 400
    except (HTTPError, URLError, timeout):
        return False


def send_email(subject: str, body: str, email_to: str):
    msg = EmailMessage()
    msg["From"] = EMAIL_FROM
    msg["To"] = email_to
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.ehlo()
        server.starttls()
        server.login(EMAIL_FROM, SMTP_PASSWORD)
        server.send_message(msg)


def main():
    if not check_url(URL_TO_CHECK, TIMEOUT_SECONDS):
        for email_to in EMAILS_TO:
            send_email(
                subject=f"ALERT: URL down - {URL_TO_CHECK}",
                body=f"The URL {URL_TO_CHECK} is not reachable right now.",
                email_to = email_to
            )
        print("Alert email sent.")
    else:
        print("URL is reachable.")


if __name__ == "__main__":
    main()

# https://github.com/satish0308/send_email.git

