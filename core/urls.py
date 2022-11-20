from django.conf import settings
from django.contrib import admin
from django.urls import include,path
from . import views
from django.conf.urls.static import static 
import os
import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

urlpatterns = [
    path(env('ADMIN_SITE'), admin.site.urls),
    path('', views.home, name='home'),
    path('store/', include('store.urls')),
    path('carts/', include('cart.urls')),
    path('accounts/', include('acounts.urls'))
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
