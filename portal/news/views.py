from django.core.mail import send_mail
from django.http import Http404, request
from django.shortcuts import render, redirect
from .models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from .forms import CreatePost
from .filters import NewsFilter
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin


class NewsList(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'news/news.html'
    ordering = '-date_time'
    paginate_by = 10

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = NewsFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class DetailNews(DetailView):
    model = Post
    context_object_name = 'item'
    template_name = 'news/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_is_author'] = True if self.get_object().author.author.id == self.request.user.id else False
            user = self.request.user
            post = self.kwargs.get('pk')
            category_list = [i.name for i in Post.objects.get(pk=post).category.all()]
            user_category = User.objects.get(pk=user.id).subscribers_set.all()
            category_sub = [i.category.name for i in user_category]
            context['category'] = list(set(category_list).difference(set(category_sub)))
        return context

    def post(self, request, *args, **kwargs):
        user = request.user
        post = self.kwargs.get('pk')

        if user.is_authenticated:
            category_list = [i.name for i in Post.objects.get(pk=post).category.all()]
            user_category = User.objects.get(pk=user.id).subscribers_set.all()
            category_sub = [i.category.name for i in user_category]
            sub_cat = list(set(category_list).difference(set(category_sub)))
        if request.POST:
            for item in sub_cat:
                if item in request.POST:
                    cat_id = Category.objects.get(name__iexact=f'{item}')
                    subscriber = Subscribers(
                        user=user,
                        category=cat_id
                    )
                    subscriber.save()
                    break

        send_mail(
            subject=f'{self.request.user} mail sending',
            message='appointment.message',
            from_email='softb0x@yandex.ru',
            recipient_list=['di.grebenev@yandex.ru']
        )

        return redirect('/')


    # def get(self, request, *args, **kwargs):
    #     try:
    #         self.object = self.get_object()
    #     except Http404:
    #         return redirect('news')
    #     context = self.get_context_data(object=self.object)
    #     return self.render_to_response(context)

    # news = get_object_or_404(Post, pk=self.kwargs.get('pk'))


class CreateNews(PermissionRequiredMixin, CreateView):
    model = Post
    template_name = 'news/create.html'
    form_class = CreatePost
    permission_required = ('news.add_post')
    success_url = '/'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'NW'
        post.author = Author.objects.get(author_id=self.request.user.pk)
        return super().form_valid(form)


class CreateArticle(PermissionRequiredMixin, CreateView):
    model = Post
    template_name = 'news/create.html'
    form_class = CreatePost
    permission_required = ('news.add_post')
    success_url = '/'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'AT'
        post.author = Author.objects.get(author_id=self.request.user.pk)
        return super().form_valid(form)


class EditNews(PermissionRequiredMixin, UpdateView):
    model = Post
    template_name = 'news/create.html'
    permission_required = ('news.change_post')
    fields = [
        'title',
        'text',
        'category'
    ]


class DeleteNews(PermissionRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('news')
    permission_required = ('news.delete_post')
    template_name = 'news/delete.html'

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            return redirect('news')
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
