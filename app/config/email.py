from fastapi import BackgroundTasks
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from app.config.settings import get_settings
import os
from pathlib import Path

settings = get_settings()

conf = ConnectionConfig(
    MAIL_USERNAME =os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD"),
    MAIL_FROM = os.getenv("MAIL_FROM"),
    MAIL_PORT = 1025,
    MAIL_SERVER = "smtp",
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = os.getenv("USE_CREDENTIALS"),
    MAIL_DEBUG=True,
    MAIL_FROM_NAME=settings.APP_NAME,
    TEMPLATE_FOLDER= "app/static/templates"
)


fm = FastMail(conf)


async def send_email(subject: str, recipients: list, template_body: dict, template_name: str,
                     background_tasks: BackgroundTasks):
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        template_body=template_body,
        subtype=MessageType.html)
    background_tasks.add_task(fm.send_message, message, template_name=template_name)
  