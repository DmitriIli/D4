from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from news.models import Subscribers


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/protect.html'

    def get_context_data(self, **kwargs):
        user_id = self.request.user.id
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        # context['e_mail'] = User.objects.get(pk=user_id).email
        context['email'] = self.request.user.email
        categories = Subscribers.objects.filter(user=self.request.user)
        context['categories'] = [item.category.name for item in categories]
        return context
