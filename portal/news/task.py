from datetime import date, timedelta

from celery import shared_task
import time

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import *


@shared_task
def hello():
    time.sleep(10)
    print("Hello, world!")


def weekly_notify():
    # day_of_weak = 8 - datetime.weekday(datetime.now())
    # next_monday = date.today() + timedelta(days=(7 - day_of_weak))
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
