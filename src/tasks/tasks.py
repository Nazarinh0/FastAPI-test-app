import smtplib
from email.message import EmailMessage
from celery import Celery

from src.config import SMTP_PASSWORD, SMTP_USER, SMTP_HOST, SMTP_PORT


celery = Celery(
    'tasks',
    broker='redis://localhost:6379',
    broker_connection_retry_on_startup=True
)


def get_email_template_report(username: str):
    email = EmailMessage()
    email['From'] = SMTP_USER
    email['To'] = username
    email['Subject'] = f"Financial Report for {username}"
    email.set_content('<div><h1>f"Report for {username}"</h1></div>')
    return email


@celery.task
def send_email_report(username: str):
    email = get_email_template_report(username)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)
