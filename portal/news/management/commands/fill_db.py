import random
from django.core.management.base import BaseCommand

from ...models import *


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Post.objects.all().delete()
        Category.objects.all().delete()
        # Comment.objects.all().delete()

        post_temlate = {
            'text': 'fish fish fish fish fish fish fish ',
        }

        posts = [Post(title=f'Публикация {i}', **post_temlate, author=Author.objects.get(pk=random.randint(1,4)))
                 for i in range(1, 101)]
        Post.objects.bulk_create(posts)

        categories = [
            Category(name=f'category name {i}') for i in range(1, 11)]
        Category.objects.bulk_create(categories)

        categories_id_list = list(
            Category.objects.values_list('id', flat=True))

        for post in Post.objects.all():

            for i in range(3):
                index = random.randint(1, 10)
                category = Category.objects.get(name=f'category name {index}')
                PostCategory.objects.create(category=category, post=post)
