from django.urls import path

from . import views

app_name = 'project'
urlpatterns = [
    path('', views.index, name='index'),
    path('uploaded_photo/', views.uploaded_photo, name='uploaded_photo'),
    path('uploaded_photo/update/', views.update, name='update')
]
