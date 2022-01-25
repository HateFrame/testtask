from django.core.mail import send_mail
from django.conf import settings


def send_liked_mail(user, partner):
    subject = "Вы понравились!"
    message = f"Вы понравились {partner.first_name}! Почта участника: {partner.email}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]

    return send_mail(subject, message, from_email, recipient_list)
