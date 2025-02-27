from django.urls import path
from .views import RegisterUser,LoginUser

urlpatterns = [
    path('api/register',RegisterUser.as_view(),name='register'),
    path('api/login',LoginUser.as_view(),name='login'),
]