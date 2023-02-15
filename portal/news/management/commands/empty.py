import random
from django.core.management.base import BaseCommand

from ...models import *


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Post.objects.all().delete()
        PostCategory.objects.all().delete()
        Category.objects.all().delete()
        # Comment.objects.all().delete()

        