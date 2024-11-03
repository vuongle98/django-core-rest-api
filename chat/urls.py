from django.urls import path, include
from rest_framework.routers import DefaultRouter

from chat import views
from django.contrib.auth import views as auth_views

from chat.views import CreateRoomView, AddUserToRoom, CreateChatMessageView
from chat.viewsets import RoomViewSet

router = DefaultRouter()
router.register(r'rooms', RoomViewSet, basename='room')

urlpatterns = [
    path('ui/<str:room_name>/', views.chat_room),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('rooms/', include(router.urls)),
]