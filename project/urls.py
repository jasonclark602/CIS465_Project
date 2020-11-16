from django.urls import path
from django.contrib import admin 
from django.urls import path 
from django.conf import settings 
from django.conf.urls.static import static 
from .views import *
urlpatterns = [
    path('', image_view, name='home'),
    path('image_upload', image_view, name = 'image_upload'), 
    path('calculations', calculations, name = 'calculations'), 
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
