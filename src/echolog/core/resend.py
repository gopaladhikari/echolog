import resend

from echolog.core.config import config

resend.api_key = config.RESEND_API_KEY


def send_email(to: str, subject: str, html: str):
    params: resend.Emails.SendParams = {
        "from": "Echolog <echolog@gopuadks.dev>",
        "to": [to],
        "subject": subject,
        "html": html,
    }

    email = resend.Emails.send(params)

    return email
