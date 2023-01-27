from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import mail_managers, send_mail
from .models import Post


@receiver(post_save, sender=Post)  # подключение сигналов с использованием декоратора
def mail_sender(sender, instance, created, recipient_list, **kwargs):
    if created:
        send_mail(
            subject=f'{instance.request.user} mail sending',
            message='appointment.message',
            from_email='softb0x@yandex.ru',
            recipient_list=recipient_list
        )

# post_save.connect(mail_sender, sender=Post) # подключение сигналов
