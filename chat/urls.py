from django.urls import path, include

from chat import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('ui/<str:room_name>/', views.chat_room),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]