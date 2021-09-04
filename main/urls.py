from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.register), 
    path('login', views.login),
    path('wall', views.wall),
    path('new_post', views.new_post),
    path('logout', views.logout),
    path('comment', views.comment)
]
