from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('news/<int:pk>/', DeteilNews.as_view(), name='detailNews'),
    path('news/create/', CreateNews.as_view(), name='createNews'),
    path('news/<int:pk>/edit/', EditNews.as_view(), name='editNews'),
    path('news/<int:pk>/delete/', DeleteNews.as_view(), name='deleteNews'),
    path('articles/create/', CreateArticle.as_view(), name='createArticle'),
    path('articles/<int:pk>/', DeteilNews.as_view(), name='detailArticle'),
    path('articles/<int:pk>/edit/', EditNews.as_view(), name='editArticle'),
    path('articles/<int:pk>/delete/', DeleteNews.as_view(), name='deleteArticle'),
]