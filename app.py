import os
import smtplib
from email.message import EmailMessage
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from socket import timeout

URL_TO_CHECK = "https://example.com"
TIMEOUT_SECONDS = 10

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587

SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
EMAIL_FROM = SMTP_USERNAME
EMAIL_TO = os.getenv("EMAIL_TO")


def check_url(url: str, timeout_seconds: int = 10) -> bool:
    try:
        with urlopen(url, timeout=timeout_seconds) as response:
            return 200 <= response.status < 400
    except (HTTPError, URLError, timeout):
        return False


def send_email(subject: str, body: str):
    msg = EmailMessage()
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.ehlo()
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)


def main():
    if not check_url(URL_TO_CHECK, TIMEOUT_SECONDS):
        send_email(
            subject=f"ALERT: URL down - {URL_TO_CHECK}",
            body=f"The URL {URL_TO_CHECK} is not reachable right now.",
        )
        print("Alert email sent.")
    else:
        print("URL is reachable.")


if __name__ == "__main__":
    main()

# https://github.com/satish0308/send_email.git

