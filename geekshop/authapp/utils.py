from django.core.mail import send_mail
from django.urls import reverse
from urllib.parse import urljoin
from django.conf import settings


def send_verification_mail(user):
    verification_link = urljoin(
        settings.SITE_ADDRESS,
        reverse(
            "auth:verify",
            args=[user.email, user.activation_key],
        ),
    )

    send_mail(
        "Verify your account",
        f"Use this link to verify your account: {verification_link}",
        "no-reply@localhost",
        [user.email],
        fail_silently=True,
    )
