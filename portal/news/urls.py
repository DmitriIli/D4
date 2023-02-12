from django.contrib import admin
from django.urls import path, include
from .views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('news/<int:pk>/', DetailNews.as_view(), name='detailNews'),
    # path('news/<int:pk>/', cache_page(300)(DetailNews.as_view()), name='detailNews'),
    path('news/create/', CreateNews.as_view(), name='createNews'),
    path('news/<int:pk>/edit/', EditNews.as_view(), name='editNews'),
    path('news/<int:pk>/delete/', DeleteNews.as_view(), name='deleteNews'),
    path('articles/create/', CreateArticle.as_view(), name='createArticle'),
    path('articles/<int:pk>/', DetailNews.as_view(), name='detailArticle'),
    # path('articles/<int:pk>/', cache_page(300)(DetailNews.as_view()), name='detailArticle'),
    path('articles/<int:pk>/edit/', EditNews.as_view(), name='editArticle'),
    path('articles/<int:pk>/delete/', DeleteNews.as_view(), name='deleteArticle'),
    path('categorylist/', CategoryAPIView.as_view()),
    path('categorylist/<int:pk>/', CategoryAPIView.as_view()),
    
]
