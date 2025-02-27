from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import path
from . import views

urlpatterns = [
    path('chat/',views.redirect_to_chat,name='chat_redirect'),
    path("api/user/", views.get_authenticated_user, name="get_authenticated_user"),
    # path("api/messages/<str:room_name>/", views.get_messages, name="get_messages")
]
