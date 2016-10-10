from django.core.mail import send_mail as _send_mail

def send_mail(key, user_email):
    return _send_mail(
        'Test Platxo',
        key,
        'admin@platxo.com',
        [user_email],
        fail_silently=False,
    )
