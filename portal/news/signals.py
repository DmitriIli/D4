from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import mail_managers, send_mail, EmailMultiAlternatives
from django.shortcuts import redirect
from django.template.loader import render_to_string

from .models import Post, Subscribers


@receiver(post_save, sender=Post)# подключение сигналов с использованием декоратора
def subscribers_notify(sender, instance, created, **kwarg):
    recipient_list = []
    categories = [i for i in Post.objects.get(pk=instance.id).category.all()]
    for item in categories:
        subscribers = Subscribers.objects.filter(category_id=item).all()
        if subscribers:
            for i in subscribers:
                recipient_list.append(User.objects.get(pk=i.user_id).email)
    email_list = list(set(recipient_list))
    email_list = [item for item in email_list if item]
    if created:
        html_content = render_to_string(
            'news/notify.html',
            {
                'instance': instance,
            }
        )
        msg = EmailMultiAlternatives(
            subject=f'{instance.title} {instance.date_time.strftime("%Y-%M-%d")}',
            body=f'{instance.text[:20]}  http://127.0.0.1:8000/news/{instance.id}',
            from_email='softb0x@yandex.ru',
            to=email_list,
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html

        msg.send()  # отсылаем
        print(email_list)

        return redirect('/')

# post_save.connect(mail_sender, sender=Post) # подключение сигналов
