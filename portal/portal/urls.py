from django.contrib import admin
from django.urls import path, include
from news.views import NewsList

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('', include('news.urls')),
    path('', NewsList.as_view(), name='news'),
    path('sign/', include('sign.urls')),
    path('', include('protect.urls'))
]
