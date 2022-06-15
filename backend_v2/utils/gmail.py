from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.utils.html import strip_tags
from django.conf import settings


def send_message(to, subject, code):
    html_content = render_to_string('account/email/password_reset_key_message.html', {'certificate_code': code})
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
