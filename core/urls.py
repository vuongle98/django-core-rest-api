from django.urls import path, include


urlpatterns = [
    path('notification/', include('core.notification.urls')),
    path('auth/', include('core.auth.urls'), name="auth"),
    path('user/', include('core.user.urls'), name='users'),
    path('menu-item/', include('core.menu.urls'), name='menu')
]