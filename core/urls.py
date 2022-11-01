from django.conf import settings
from django.contrib import admin
from django.urls import include,path
from django import views
from django.conf.urls.static import static 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('store/', include('store.urls')),
    path('carts/', include('carts.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
