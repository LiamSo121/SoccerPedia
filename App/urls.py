from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/',views.about,name='about'),
    path('register/',views.register,name='register'),
    path('login/',views.user_login,name='user_login'),
    path('user_logout/', views.user_logout, name='user_logout')
]

