from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from news.models import Author
from django.contrib.auth.models import User, Group
from django.views.generic.edit import CreateView
from .forms import BaseRegisterForm


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/sign/login/'


@login_required
def make_author(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
        author = Author.objects.create(author=user)
    return redirect('/')
