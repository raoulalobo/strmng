from django.urls import path
from . import views


app_name = 'videos_app'
urlpatterns = [

    #URL
    path('home', views.home, name='home'),
    path('list', views.list, name='list'),
    path('test', views.test, name='test'),
    #path('list/<movie_id>', views.list, name='list'),
    path('single/<movie_id>', views.single, name='single'),
]