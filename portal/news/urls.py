from django.contrib import admin
from django.urls import path, include
from .views import *
from django.views.decorators.cache import cache_page
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'category', CategoryViewSet) 

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
    path('api/v1/', include(router.urls)),# http://127.0.0.1:8000/api/v1/category/

    # path('api/v1/categorylist/', CategoryViewSet.as_view({'get':'list'})),
    # path('api/v1/categorylist/<int:pk>/', CategoryViewSet.as_view({'put':'update'})),
    # path('api/v1/categorylist/', CategoryAPIList.as_view()),
    # path('api/v1/categorylist/<int:pk>/', CategoryAPIView.as_view()),
    # path('api/v1/categorydetail/<int:pk>/', CategoriAPIDetailView.as_view()),
    
]
