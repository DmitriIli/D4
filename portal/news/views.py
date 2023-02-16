from datetime import timedelta
from django.forms import model_to_dict
from django.http import Http404, request
from django.shortcuts import render, redirect
from .models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from .forms import CreatePost
from .filters import NewsFilter
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.cache import cache
from rest_framework import viewsets, generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, UpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from .utils import query_debugger


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
            context['user_is_author'] = True if self.get_object(
            ).author.author.id == self.request.user.id else False
            user = self.request.user
            post = self.kwargs.get('pk')
            category_list = [i.name for i in Post.objects.get(
                pk=post).categories.all()]
            user_category = User.objects.get(pk=user.id).subscribers_set.all()
            category_sub = [i.category.name for i in user_category]
            context['category'] = list(
                set(category_list).difference(set(category_sub)))
        return context

    def post(self, request, *args, **kwargs):
        user = request.user
        post = self.kwargs.get('pk')
        if user.is_authenticated:
            category_list = [i.name for i in Post.objects.get(
                pk=post).categories.all()]
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
        return redirect('/')

    def get_object(self, *args, **kwargs) -> models.Model:
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj

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
        'categories'
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


# class CategoryAPIView(APIView):
#     def get(self,request):

#         cat = Category.objects.all()
#         return Response({'categories':CategorySerializers(cat, many=True).data})

#     def post(self, request):
#         serilizer = CategorySerializers(data=request.data) #переданы один аргумент, вызывается метод create класса CategorySerializers
#         serilizer.is_valid(raise_exception=True)
#         # cat_new =  Category.objects.create(
#         #     name = request.data['name']
#         # )
#         # return Response({'category': CategorySerializers(cat_new).data})
#         serilizer.save()
#         return Response({'category': serilizer.data})

#     def put(self, request, *args, **kwargs):
#         pk = kwargs.get('pk', None)
#         if not pk:
#             return Response({'errore':'Method put is not allowed'})
#         try:
#             instance = Category.objects.get(pk=pk)
#         except:
#             return Response({'error':'Object does not exist'})

#         serializer = CategorySerializers(data = request.data, instance=instance) #переданы два аргумента, вызывается метод update класса CategorySerializers
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({'data':serializer.data})


#     def delete(self, request, format=None,*args, **kwargs):
#         pk = kwargs.get('pk', None)
#         if not pk:
#             return Response({'error':'Method delete is not allowed'})
#         try:
#             instance = Category.objects.get(pk=pk)
#         except:
#             return Response({'error':'object does not exist'})
#         instance.delete()
#         return Response({'post':'delete post '+str(pk)},status=status.HTTP_204_NO_CONTENT)


### build-in view DRM ###
# class CategoryAPIList(ListCreateAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategoryModelSerializers

# class CategoryAPIView(UpdateAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategoryModelSerializers

# class CategoriAPIDetailView(RetrieveUpdateDestroyAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategoryModelSerializers

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostModelSerialisers
    pagination_class = StandardResultsSetPagination


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializers

@query_debugger
def posts():
    # qs = Post.objects.all()
    # qs = Post.objects.all().select_related('author')
    qs = (
        Post.objects.select_related('author').values('title','author__author__username')
        # Post.objects.all().select_related('author').prefetch_related('categories').values_list('title','author__author__username', 'categories')
    )
    # qs = Post.objects.prefetch_related('categories')
    print('---------------------')
    print(qs.query)
    print('---------------------')
    p = []
    # for item in qs.values:
    #     p.append({
    #         'author': item.author,
    #         'title': item.title[:5],
    #         # 'text': item.text[:10],
    #         # 'categories':item.categories,
    #     })
    # print(p)
    print('---------------------')
    print(qs.values_list)
    print('---------------------')
    return p