from celery import shared_task
from splitwise.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

@shared_task(bind=True)
def send_mail_task(self,mail_subject,message,to_mail):
    send_mail(
        subject=mail_subject,
        message=message,
        from_email=EMAIL_HOST_USER,
        recipient_list=[to_mail],
        fail_silently=True,
    )
    return True