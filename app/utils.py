from dataclasses import dataclass
from jinja2 import Template
from app.settings import settings
from pathlib import Path
import emails


@dataclass
class EmailData:
    html_content: str
    subject: str


def render_email_template(template_name: str, context: dict) -> str:
    template_str = (
        Path(__file__).parent / "email-templates" / "build" / template_name
    ).read_text()
    html_content = Template(template_str).render(context)
    return html_content


def generate_new_account_email(
    email_to: str, username: str, password: str
) -> EmailData:
    subject = f"New account for {username}"
    html_content = render_email_template(
        template_name="new_account.html",
        context={
            "username": username,
            "password": password,
            "email": email_to,
        },
    )
    return EmailData(html_content=html_content, subject=subject)


def send_email(email_to: str, subject: str = "", html_content: str = "") -> None:
    # Validate required settings
    if not settings.SMTP_HOST:
        raise ValueError("SMTP_HOST is not configured")
    if not settings.EMAILS_FROM_EMAIL:
        raise ValueError("EMAILS_FROM_EMAIL is not configured")

    message = emails.Message(
        subject=subject,
        html=html_content,
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    elif settings.SMTP_SSL:
        smtp_options["ssl"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD

    try:
        response = message.send(to=email_to, smtp=smtp_options)
        # Check if response indicates failure
        if response is None:
            raise Exception("Failed to send email: No response from SMTP server")
        if hasattr(response, "status_code"):
            if response.status_code != 250:
                error_msg = getattr(response, "error", "Unknown error")
                raise Exception(
                    f"Failed to send email. SMTP status code: {response.status_code}, "
                    f"Error: {error_msg}"
                )
    except Exception as e:
        # Log the exception or handle it as needed
        print(f"Exception occurred while sending email: {e}")
        raise e
