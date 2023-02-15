from django.contrib import admin
from django.urls import path, include
from .views import *
from django.views.decorators.cache import cache_page
from rest_framework import routers

# basrname=<name_queryset> соответсвует имени запроса в базу queryset
# basename не требуется, если во view определен queryset. если же queryset не задан явно, то basename необходимо задать 

router_category = routers.SimpleRouter()
router_category.register(r'category', CategoryViewSet, basename='category') 

router_post = routers.SimpleRouter()
router_post.register(r'news', PostViewSet, basename='post')


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
    path('api/v1/', include(router_category.urls)),# http://127.0.0.1:8000/api/v1/category/
    path('api/v1/', include(router_post.urls)),# http://127.0.0.1:8000/api/v1/post/
    # path('api/v1/categorylist/', CategoryViewSet.as_view({'get':'list'})),
    # path('api/v1/categorylist/<int:pk>/', CategoryViewSet.as_view({'put':'update'})),
    # path('api/v1/categorylist/', CategoryAPIList.as_view()),
    # path('api/v1/categorylist/<int:pk>/', CategoryAPIView.as_view()),
    # path('api/v1/categorydetail/<int:pk>/', CategoriAPIDetailView.as_view()),
    
]
print(router_post)