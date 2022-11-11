from django.core.mail import send_mail


def send_email(data):
    return send_mail(
        data['subject'],
        None,
        data['from'],
        data['to'],
        fail_silently=False,
        html_message=data['html'],
    )
