from datetime import date, timedelta
from celery import shared_task
import time
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from .models import *
from ..portal.celery import app



@shared_task
def weekly_notify():
    # day_of_weak = 8 - datetime.weekday(datetime.now())
    # next_monday = date.today() + timedelta(days=(7 - day_of_weak))

    
    # получить список адрсов подписчиков по категориям
    # email_list = set()        
    # category_list = Category.objects.all()
    # for category in category_list:
    #     for item in category.subscribers_set.all():
    #         email_list.add(item.user.email)

    week_ago = date.today() - timedelta(days=7)
    post_list = Post.objects.filter(date_time__gte=datetime.now() - timedelta(days=7))
    email_list = set()
    for item in post_list:
        for category in item.categories.all():
            subscribers = Subscribers.objects.filter(category_id=category).all()
            if subscribers:
                for i in subscribers:
                    email_list.add(User.objects.get(pk=i.user_id).email)

    subject, from_email, to = 'рассылка', 'softb0x@yandex.ru', email_list

    posts = []

    for post in post_list:
        if Post.objects.get(title=post).date >= week_ago:
            posts.append(Post.objects.get(title=post))

    if posts and email_list:
        html_content = render_to_string(
            'news/mailing_list.html',
            {
                'posts': posts,
            }
        )
        msg = EmailMultiAlternatives(
            subject=subject,
            body=' ',  # это то же, что и message
            from_email=from_email,
            to=email_list,  # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html

        msg.send()  # отсылаем

@app.task()
def add_news_notify(pk):
    email_list = set()
    post = Post.objects.get(pk=pk)
    categories = post.category_set.all()
    for category in categories:
        for item in category.subscribers_set.all():
            email_list.add(item.user.email)        
    send_mail(
        subject=f'{post.title}',
        message=f'{post.text[:20]}',
        from_email='softb0x@yandex.ru',
        recipient_list=list(email_list),
    )

@receiver(post_save, sender=User)
def adduser_message(sender, instance, created, **kwarg):
    if created:
        html_content = render_to_string(
            'news/add_new_user.html',
            {
                'instance': instance,
            }
        )

        msg = EmailMultiAlternatives(
            subject=f'Приветсвую тебя {instance.name}',
            body=f'Приветсвенное письмо для нового пользователя {instance.name}',
            from_email='softb0x@yandex.ru',
            to=instance.email,
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html

        msg.send()  # отсылаем

        return redirect('/')


@receiver(post_save, sender=Post)
def send_notify_add_post(sender, instance, signal, created, *args, **kwargs):
    if created:
        add_news_notify.delay(instance.pk)