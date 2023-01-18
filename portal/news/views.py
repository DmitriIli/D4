from django.http import Http404, request
from django.shortcuts import render, redirect
from .models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from .forms import CreatePost
from .filters import NewsFilter


class NewsList(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'news/news.html'
    ordering = '-date_time'
    paginate_by = 2


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
        print(self.request.user)
        return context


class DeteilNews(DetailView):
    model = Post
    context_object_name = 'item'
    template_name = 'news/detail.html'

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            return redirect('news')
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    # news = get_object_or_404(Post, pk=self.kwargs.get('pk'))


class CreateNews(CreateView):
    model = Post
    template_name = 'news/create.html'
    form_class = CreatePost
    success_url = '/'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'NW'
        return super().form_valid(form)


class CreateArticle(CreateView):
    model = Post
    template_name = 'news/create.html'
    form_class = CreatePost
    success_url = '/'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'AT'
        return super().form_valid(form)


class EditNews(UpdateView):
    model = Post
    template_name = 'news/create.html'
    fields = [
        'author',
        'title',
        'text',
        'category'
    ]


class DeleteNews(DeleteView):
    model = Post
    success_url = reverse_lazy('news')
    template_name = 'news/delete.html'

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            return redirect('news')
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    class CreateNews(CreateView):
        model = Post

        # form_class = CreateForm
        # initial = {'': '0'}
        template_name = 'news/create.html'
        fields = [
            'author',
            'title',
            'text',
            'category'
        ]

    class EditNews(UpdateView):
        model = Post
        template_name = 'news/create.html'
        fields = [
            'author',
            'title',
            'text',
            'category'
        ]

    class DeleteNews(DeleteView):
        model = Post
        success_url = reverse_lazy('news')
        template_name = 'news/delete.html'

        def get(self, request, *args, **kwargs):
            try:
                self.object = self.get_object()
            except Http404:
                return redirect('news')
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)


class CreateArticle(CreateView):
    model = Post

    # form_class = CreateForm
    # initial = {'': '0'}
    template_name = 'news/create.html'
    fields = [
        'author',
        'title',
        'text',
        'category'
    ]


class EditArticle(UpdateView):
    model = Post
    template_name = 'news/create.html'
    fields = [
        'author',
        'title',
        'text',
        'category'
    ]


class DeleteArticle(DeleteView):
    model = Post
    success_url = reverse_lazy('')
    template_name = 'news/delete.html'

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            return redirect('news')
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
