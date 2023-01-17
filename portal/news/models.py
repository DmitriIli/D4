from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from datetime import datetime
from django.urls import reverse, reverse_lazy


class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.author.username

    class Meta:
        pass

    def update_rating(self):
        rating_post = self.post_set.aggregate(post_rating=Sum('rating'))
        r_post = 0
        r_post += rating_post.get('post_rating')

        rating_comment = self.author.comment_set.aggregate(comment_rating=Sum('rating'))
        r_comment = 0
        r_comment += rating_comment.get('comment_rating')

        self.rating = r_post * 3 + r_comment
        self.save()


class Category(models.Model):
    name = models.CharField(unique=True, max_length=64)

    def __str__(self):
        return f'{self.name}'


class Post(models.Model):

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, default='AT')
    date_time = models.DateTimeField(auto_now=True)
    category = models.ManyToManyField(Category)
    title = models.CharField(max_length=64, default=f'статья от {datetime.now()}')
    text = models.TextField(default='содердание статьи')
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.title}:\n' \
               f'{self.date_time}, ' \
               f'{self.text[:20]}...'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[:123]}...'

    def get_absolute_url(self):
        return reverse_lazy('news')



class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=256, default='текс комментария')
    date_time = models.DateTimeField(auto_now=True)
    rating = models.SmallIntegerField(default=0)
