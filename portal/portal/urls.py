from django.contrib import admin
from django.urls import path, include
from news.views import NewsList
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('', include('news.urls')),
    path('', (NewsList.as_view()), name='news'),
    # path('', cache_page(60)(NewsList.as_view()), name='news'),
    path('sign/', include('sign.urls')),
    path('', include('protect.urls'))
]
