from django.urls import path, include
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls', namespace='blog')), # вреЕменная заглушка для перенаправления в blog из корня сайта
    path('blog/', include('blog.urls', namespace='blog')),
]
