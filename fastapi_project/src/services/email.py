from pathlib import Path
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr
from fastapi_project.src.conf.config import config
from fastapi_project.src.services.auth import auth_service

conf = ConnectionConfig(
    MAIL_USERNAME=config.MAIL_USERNAME,
    MAIL_PASSWORD=config.MAIL_PASSWORD,
    MAIL_FROM=config.MAIL_USERNAME,
    MAIL_PORT=config.MAIL_PORT,
    MAIL_SERVER=config.MAIL_SERVER,
    MAIL_FROM_NAME=config.MAIL_FROM_NAME,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / 'templates',
)


async def send_email(email: EmailStr, username: str, host: str):
    """
    Sends a confirmation email to the user.

    This function sends an email with a verification token and a confirmation
    link to the specified email address.

    :param email: Email address of the recipient.
    :type email: EmailStr
    :param username: Username of the recipient.
    :type username: str
    :param host: Base URL or domain to be used in the confirmation link.
    :type host: str
    :raises ConnectionErrors: If sending the email fails due to a connection issue.
    """
    try:
        token_verification = auth_service.create_email_token({"sub": email})
        message = MessageSchema(
            subject="Confirm your email ",
            recipients=[email],
            template_body={"host": host, "username": username, "token": token_verification},
            subtype=MessageType.html
        )

        fm = FastMail(conf)
        await fm.send_message(message, template_name="email_template.html")
    except ConnectionErrors as err:
        print(err)

async def send_rp_email(email: EmailStr, username: str, host: str):
    """
    Sends a password reset email to the user.

    This function sends an email containing a reset token and a link to reset
    the password.

    :param email: Email address of the recipient.
    :type email: EmailStr
    :param username: Username of the recipient.
    :type username: str
    :param host: Base URL or domain to be used in the reset link.
    :type host: str
    :raises ConnectionErrors: If sending the email fails due to a connection issue.
    """
    try:
        token_verification = auth_service.create_email_token({"sub": email})
        message = MessageSchema(
            subject="Reset your email ",
            recipients=[email],
            template_body={"host": host, "username": username, "token": token_verification},
            subtype=MessageType.html
        )

        fm = FastMail(conf)
        await fm.send_message(message, template_name="email_rp_template.html")
    except ConnectionErrors as err:
        print(err)


